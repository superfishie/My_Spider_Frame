#coding:utf-8

import gevent.monkey
from gevent.pool import Pool as BasePool
gevent.monkey.patch_all()

#实现自定义的方法实现接口兼容
class Pool(BasePool):
    #协程和线程都有同名参数
    def apply_async(self,func,args=None,kwds=None,callback=None):
        return BasePool().apply_async(func=func,args=args,kwds=kwds,callback=callback)

    def close(self):
        pass
