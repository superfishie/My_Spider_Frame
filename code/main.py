#coding:utf-8
from Screepy.core.engine import Engine

# from spiders.baidu import BaiduSpider
# from spiders.douban import DoubanSpider
#
# from pipelines import BaiduPipeline1,BaiduPipeline2,DoubanPipeline1,DoubanPipeline2
#
# from middlewares import SpiderMiddleware1,SpiderMiddleware2,DownloaderMiddleware1,DownloaderMiddleware2



def main():
    # baidu_spider = BaiduSpider()
    # douban_spider = DoubanSpider()
    #
    # spiders = {"baidu":baidu_spider,"douban": douban_spider}
    #
    # pipelines = [BaiduPipeline1(),BaiduPipeline2(),
    #              DoubanPipeline1(),DoubanPipeline2()]
    #
    # #通过自定义middlewares构建了多个爬虫中间件
    # spider_middlewares = [SpiderMiddleware1(),SpiderMiddleware2()]
    #
    # #通过自定义middlewares构建了多个下载中间件
    # downloader_middlewares = [DownloaderMiddleware1(),DownloaderMiddleware2()]
    #
    # engine = Engine(spiders,
    #                 pipelines=pipelines,
    #                 spider_mids=spider_middlewares,
    #                 downloader_mids=downloader_middlewares)

    engine = Engine()
    engine.start()

    # import redis
    # from Screepy.http.request import Request

    # import pickle
    # import json

    # json.dumps():将python数据类型转为json字符串
    # json.loads():将json字符串转为python数据类型

    # pickle.dumps():将python数组转为二进制字符串
    # pickle.load(): 将二进制字符串转为python数据类型

    # client = redis.Redis(db=2)
    #
    # key = "fingerprint_set"
    #
    # client.sadd

    #类对象 = getattr(文件中的绝对路径名,"文件中类名")


if __name__ == '__main__':
   main()

