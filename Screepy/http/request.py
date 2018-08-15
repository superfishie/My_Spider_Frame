#coding:utf-8

class Request(object):

    '''
        框架自定义的请求类,用户可以通过这个类构建请求对象
    '''
    def __init__(self,url,method="GET",headers=None,params=None,data=None,proxy=None,callback='parse',dont_filter=False):
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
        self.proxy = proxy
        self.callback = callback #该请求发送后的回调函数
        self.dont_filter = dont_filter