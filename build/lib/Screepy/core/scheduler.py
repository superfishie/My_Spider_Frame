#coding:utf-8
import six

from ..utils.log import logger
from ..conf.default_settings import *

#如果是分布式的角色,那么使用redis数据库的队列
if role == "master" or role == "slave":
    from ..utils.queue import Queue
    from ..utils.set import RedisFilterSet as Set
elif role == None:
    try:
        from queue import Queue
    except ImportError:
        from Queue import Queue
    from ..utils.set import NormalFilterSet as Set
else:
    raise Exception("Not Support role : {}".format(role))


# from six.moves.queue import Queue

class Scheduler(object):
    def __init__(self):
        #构建保存请求对象的 请求队列
        self.queue = Queue()
        self.filter_set = Set()

        self.total_request = 0


    def add_request(self,request):
        fp = self._get_fingerprint(request)
        if self.filter_set.is_filter(request,fp):
            self.queue.put(request)
            self.filter_set.add(fp)

            self.total_request += 1



    def get_request(self):
        #从请求队列中取出一个请求:FIFO
        # self.queue.get()#如果没有数据会导致程序阻塞
        try:
            return self.queue.get(False) #如果没数据会抛出异常
        except:
            return None


    # def _filter_request(self,request,fp):
    #     #如果该请求的url在集合中,表示该请求不需要放入请求队列,返回False表示不同意放入队列
    #     if fp in self.filter_set:
    #         logger.info("Filter Request: <{}>".format(request.url)) #去重提示
    #         return False
    #     else:
    #         #如果请求的url不在集合中,则同意放入请求队列
    #         return True

    #用sha1对request做处理,返回请求指纹;sha1
    def _get_fingerprint(self,request):
        from hashlib import sha1
        url = self._get_utf8_str(request.url)
        method = self._get_utf8_str(request.method.upper())

        params = request.params if request.params else {}
        params = str(sorted(params.items(),key=lambda x : x[0]))

        data = request.data if request.data else {}
        data = self._get_utf8_str(str(sorted(data.items(),key=lambda x:x[0])))

        sha1_data = sha1()

        sha1_data.update(url)
        sha1_data.update(method)
        sha1_data.update(params)
        sha1_data.update(data)

        fp = sha1_data.hexdigest()

        return fp


    def _get_utf8_str(self,string):
        """
        如果字符串是unicode,返回utf-8
        如果字符串不是unicode,返回原字符串
        """
        if six.PY2:
            if isinstance(string,unicode):
                return string.encode("utf-8")
            else:
                return string
        else:
            if isinstance(string,str):
                return string.encode("utf-8")
            else:
                return string




