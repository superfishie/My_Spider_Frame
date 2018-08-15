#coding:utf-8

from ..http.request import Request
from ..http.item import Item

class Spider(object):

    name = None

    # start_url = "http://www.baidu.com"
    start_urls = []
    def __init__(self):
        if self.name is None:
            raise Exception("Must have a spider name.")

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)

    def parse(self, response):
        raise Exception("Must overwrite this parse func.")


