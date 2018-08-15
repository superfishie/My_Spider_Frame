#coding:utf-8
import time
from datetime import datetime

from spider import Spider
from scheduler import Scheduler
from downloader import Downloader
from pipeline import Pipeline


from ..http.item import Item
from ..http.request import Request

from ..middeware.downloader_middleware import DownloaderMiddleware
from ..middeware.spider_middleware import SpiderMiddleware

from ..utils.log import logger

from ..conf.default_settings import *

if ASYNC_TYPE == "thread":
    from multiprocessing.dummy import Pool
elif ASYNC_TYPE == "coroutine":
    from ..async.coroutine import Pool
else:
    raise Exception("No Support async type : {}".format(ASYNC_TYPE))



class Engine(object):
    def __init__(self):
        # self.spiders = spiders
        self.spiders = self._auto_import_module(SPIDERS,True)

        self.scheduler = Scheduler()

        self.downloader = Downloader()
        # self.pipelines = pipelines
        self.pipelines = self._auto_import_module(PIPELINES)

        self.spider_mids = self._auto_import_module(SPIDER_MIDDLEWARES)

        self.downloader_mids = self._auto_import_module(DOWNLOADER_MIDDLEWARES)

        self.pool = Pool()

        self.total_response = 0

        self.is_running = True

    def _auto_import_module(self,module_list,spider=False):
        #如果是爬虫进行动态模块导入,就创建字典保存所有的对象{spider.name: spider_obj}
        if spider:
            instance = {}
        #如果不是爬虫,就创建列表保存[p1,p2]
        else:
            instance = []

        import importlib

        for module in module_list:
            path_name = module[:module.rfind(".")]
            class_name = module[module.rfind(".")+1:]
            path = importlib.import_module(path_name)

            cls = getattr(path,class_name)
            if spider:
                instance[cls.name] = cls()
            else:
                instance.append(cls())

        return instance



    def start(self):
        start = datetime.now()
        logger.info("Start time : {}".format(start))

        self._start_engine()

        end = datetime.now()
        logger.info("End time : {}".format(end))

        logger.info("Using time: {}".format((end - start).total_seconds()))

    def _callback(self,_):
        #当is_running为True,表示允许一直递归调用自身处理请求
        #当处理的总请求数和响应数相同, is_running被设置为False,则递归停止
        if self.is_running == True:
            print("the queue is getting requests..")
            self.pool.apply_async(self._execute_request_response_item,callback=self._callback)


    def _start_engine(self):
        logger.info("Async Type is {}".format(ASYNC_TYPE))

        if role == "master" or role is None:
            print("Role is {}".format(role))
            #将start_rqeuest请求存入调度器
            self._execute_start_engine()
        if role == "slave" or role is None:
            print("Role is {}".format(role))
            #创建一个子线程执行这一部分代码
            for _ in range(ASYNC_COUNT):
                self.pool.apply_async(self._execute_request_response_item,callback=self._callback)
            #从调度器中取出请求,发送请求解析响应(涉及网络IO)
        # self._execute_request_response_item()


        #主线程等子线程,直到所有请求处理完成
        while True:
            #当调度器里添加的总请求数和引擎解析的总响应数相同时,表示所有请求处理完毕,此时主线程才可以继续执行
            time.sleep(0.01) #降低cpu占用,避免cpu疯狂空转
            if self.scheduler.total_request == self.total_response and self.scheduler.total_request != 0:
                print('total responses are:', self.total_response)
                print("total requests are:", self.scheduler.total_request)
                #当if条件满足时,停止callback的递归调用
                self.is_running = False
                break

        self.pool.close()
        self.pool.join()

        logger.info("Main thread is over")


    def _execute_start_engine(self):
        #1.先调用spider对象的start_request()方法,获取第一批入口请求
        for spider_name,spider in self.spiders.items():
            for start_request in spider.start_requests():
                start_request.spider = spider.name  #将爬虫名赋给请求的属性(虽然这个属性事先没有定义)

                for spider_mid in self.spider_mids:
                    # 1.1 将请求通过爬虫中间件做预处理
                    start_request = spider_mid.process_request(start_request)

                #2.将第一批通过爬虫中间件处理好的入口请求交给调度器处理并保存
                self.scheduler.add_request(start_request)

    def _execute_request_response_item(self):
        #3.将调度器中处理好的请求取出
        request = self.scheduler.get_request()

        #4-.请求发送前,通过下载中间件做预处理
        for downloader_mid in self.downloader_mids:
            request = downloader_mid.process_request(request)

        #4.将请求交给下载器的send_request()发送请求,返回响应
        response = self.downloader.send_request(request)

        #4+.下载器返回响应交给parse解析前,经过下载中间件做预处理
        for downloader_mid in self.downloader_mids:
            response = downloader_mid.process_response(response)

        #5.将response 响应交给spider的parse()解析,并返回解析结果
        spider_name = request.spider  # 将请求的属性里的爬虫名再赋值回来
        spider = self.spiders[spider_name]  #根据爬虫名取出爬虫对象
        # 通过request对象的callback参数调用解析方法, 默认callback='parse'
        parse_func = getattr(spider,request.callback)

        for result in parse_func(response): #每个for处理一个响应

            #6. 判断解析结果:若为请求对象,则交给调度器处理
            if isinstance(result,Request):

                for spider_mid in self.spider_mids:
                #6.1 请求通过爬虫中间件做预处理
                    result = spider_mid.process_request(result)
                result.spider = spider_name #爬虫名赋给中间件处理过的请求属性
                self.scheduler.add_request(result)

            #若为Item对象, 交给管道的process_item()方法处理
            elif isinstance(result,Item):
                # 6.2 item交给每一个爬虫中间件做预处理
                for spider_mid in self.spider_mids:
                    result = spider_mid.process_item(result)
                # 再将item交给每一个管道做处理
                for pipeline in self.pipelines:
                    result =  pipeline.process_item(result,spider)
            # 如果既不是请求也不是item,就抛出异常报错
            else:
                raise Exception("Not Support data type : <{}>".format(type(result)))

        self.total_response += 1
