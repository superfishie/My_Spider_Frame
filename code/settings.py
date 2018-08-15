#coding: utf-8

DEFAULT_LOG_FILENAME = 'baidu.log'


SPIDERS = [
    "spiders.baidu.BaiduSpider",
    "spiders.douban.DoubanSpider"
]

PIPELINES = [
        #"pipelines.BaiduPipeline1",
        # "pipelines.BaiduPipeline2",
        # "pipelines.DoubanPipeline1",
        # "pipelines.DoubanPipeline2"
]


SPIDER_MIDDLEWARES = [
    "middlewares.SpiderMiddleware1",
    #"middlewares.SpiderMiddleware2"
]
#
# DOWNLOADER_MIDDLEWARES = [
#     "middlewares.DownloaderMiddleware1",
#     "middlewares.DownloaderMiddleware2"
# ]

ASYNC_TYPE = "thread"
#ASYNC_TYPE = "coroutine"

ASYNC_COUNT = 3

#非分布式的角色
#role = None

#分布式的角色
#role = "master"
role = "slave"


# redis队列默认配置
REDIS_QUEUE_NAME = 'request_queue'
REDIS_QUEUE_HOST = 'localhost'
REDIS_QUEUE_PORT = 6379
REDIS_QUEUE_DB = 10

#redis指纹集合的默认配置
REDIS_SET_NAME = 'request_set'
REDIS_SET_HOST = 'localhost'
REDIS_SET_PORT = 6379
REDIS_SET_DB = 10
