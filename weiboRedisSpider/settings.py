# -*- coding: utf-8 -*-

# Scrapy settings for wbSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html


# 启动爬虫用scrapy runspider weibo.py
# 开始爬虫需要在redis中push起始连接，用
# lpush weibospider:start_urls 后面加爬取的起始连接，多个用空格隔开
#  启动爬虫前，需要保证：
# redis正确配置并启动
# mongodb正确配置并启动
# 各个性化设置项是否已经设置妥当

BOT_NAME = 'weiboRedisSpider'

SPIDER_MODULES = ['weiboRedisSpider.spiders']
NEWSPIDER_MODULE = 'weiboRedisSpider.spiders'

# 默认User-Agent，这里使用Google bot的User-Agent
USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# 日志文件
# LOG_FILE = "weibo.log"
# LOG_INFO = "DEBUG"

# 指定数据库的主机ip和端口号
REDIS_HOST = '192.168.123.148'
REDIS_PORT = 6379
# 如果指定了redis的db，在启动爬虫后，lpush weibospider:start_urls连接的前，需要先切换select 2。
REDIS_PARAMS = {
    # 'password': '123456',
    'db': 2
}

# mongodb 配置
MONGODB_HOST = '192.168.123.148'
MONGODB_PORT = 27017
# MONGODB_DB_NAME = 'weibo-redis'
MONGODB_DB_NAME = 'weibo-redis-1-year'
MONGODB_SHEET_WEIBO = 'weibo'
MONGODB_SHEET_USER = 'user'
MONGODB_SHEET_UID = 'uid'

# 爬取粉丝uid和关注uid的深度
FANS_FOLLOWERS_DEPTH = 10
# 限制微博的时间，比这个日期更老的微博就不抓取了
# WEIBO_DEADLINE = "2015-06-08 00:00:00"
WEIBO_DEADLINE = "2017-07-01 00:00:00"
# 代理获取间隔，每个多少个请求获取一次ip代理，控制获取代理的速度，减少获取代理等待的时间
GET_PROXY_INTERVAL = 30
# 是否将数据写入文件
WRITE_TO_FILE = True
# 爬虫所运行的主机的名字
MACHINE_NAME = "mac"

# 使用scrapy-redis调度器组件
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 使用scrapy-redis去重组件
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 允许暂停，redis请求记录不丢失
SCHEDULER_PERSIST = True
# 默认的scrapy-redis请求集合
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    #    'weiboRedisSpider.middlewares.WbspiderSpiderMiddleware': 543,
    'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 随机选择ip代理
    'weiboRedisSpider.middlewares.RandomProxyMiddleware': 100,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'weiboRedisSpider.pipelines.WeiboredisspiderPipeline': 300,
    # 支持将数据库存储到Redis数据库里面，必须启动。是为了后续将redis中的数据保存到MongoDB中
    # 'scrapy_redis.pipelines.RedisPipeline': 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
