#coding:utf-8

from Screepy.core.spider import Spider
from Screepy.http.item import Item

class BaiduSpider(Spider):

    name = "baidu"

    start_urls = [
        "http://news.baidu.com",
        "http://www.baidu.com",
        "http://www.baidu.com",
    ]

    def parse(self,response):

        text = response.xpath("//title/text()")[0]

        data = {}
        data['title'] = text
        data['url'] = response.url
        data['content'] = len(response.body)
        item = Item(data)
        yield item

