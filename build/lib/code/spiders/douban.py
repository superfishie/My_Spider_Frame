#coding:utf-8

from Screepy.core.spider import Spider
from Screepy.http.request import Request
from Screepy.http.item import Item

class DoubanSpider(Spider):

    name = "douban"

    start_urls = [
        "https://movie.douban.com/top250?start=0",
        "https://movie.douban.com/top250?start=25",
        "https://movie.douban.com/top250?start=50"

    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)

    def parse(self,response):

        node_list = response.xpath("//div[@class='hd']")

        for node in node_list:
            data = {}
            # 电影标题
            data['title'] = node.xpath("./a/span[1]/text()")[0]
            # 详情页链接
            data['url'] = node.xpath("./a/@href")[0].encode('utf-8')

            # 返回Item对象和Request对象给引擎
            # 如果是Item对象交给管道处理
            # 如果是Request对象，通过getattr获取解析方法处理对应的响应
            yield Item(data)
            yield Request(data['url'], callback="parse_page")

    def parse_page(self,response):
        data = {}
        data['parse_page'] = response.url
        yield Item(data)