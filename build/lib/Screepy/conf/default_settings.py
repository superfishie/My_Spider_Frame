#coding:utf-8
import logging

DEFAULT_LOG_LEVEL = logging.INFO    # 默认等级
DEFAULT_LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'   # 默认日志格式
DEFUALT_LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'  # 默认时间格式
DEFAULT_LOG_FILENAME = 'xx.log'    # 默认日志文件名称

SPIDERS = []

PIPELINES = []

SPIDER_MIDDLEWARES = []

DOWNLOADER_MIDDLEWARES = []

ASYNC_TYPE = ""

ASYNC_COUNT = 1

# redis队列默认配置
REDIS_QUEUE_NAME = 'request_queue'
REDIS_QUEUE_HOST = 'localhost'
REDIS_QUEUE_PORT = 6379
REDIS_QUEUE_DB = 10

role = None

#redis指纹集合的默认配置
REDIS_SET_NAME = 'request_set'
REDIS_SET_HOST = 'localhost'
REDIS_SET_PORT = 6379
REDIS_SET_DB = 10


# 读取的是用户目录下的setttings文件,如果文件中有重名的变量,则覆盖之前的变量
from settings import *
