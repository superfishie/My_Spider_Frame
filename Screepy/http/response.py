#coding:utf-8

from lxml import etree
import re
import json


class Response(object):
    '''
        框架自定义的响应类,用户发送请求后,框架会通过这个类构建响应对象交给用户
    '''
    def __init__(self,url,status_code,headers,body,encoding):
        self.url = url
        self.status_code = status_code
        self.headers = headers
        self.body = body
        self.encoding = encoding

    def xpath(self,rule):
        html_obj = etree.HTML(self.body)
        return html_obj.xpath(rule)

    def re_findall(self,rule,string=None):
        if string is None:
            return re.findall(rule,self.body)
        else:
            return re.findall(rule,string)

    @property
    def json(self):
        '''
         可以将json文件的响应解析为对应的python数据类型并返回
         如果不是json文件则抛出异常
        '''
        try:
            return json.loads(self.body)
        except Exception as e:
            raise e






