from proxy_crawler import Crawler
from proxy_redis import IPProxyRedis

import logging

POOL_UPPER_THRESHHOLD = 10000

'''
存储proxy到redis
'''
class IPProxyGetter:
    def __init__(self):
        self.crawler = Crawler()
        self.proxy_redis = IPProxyRedis()

    def is_over_threshhod(self):
        if self.proxy_redis.count() >= POOL_UPPER_THRESHHOLD:
            return True
        else:
            return False

    def run(self):
        logging.info("proxy 获取器开始执行")
        if not self.is_over_threshhod():
            for idx in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[idx]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.proxy_redis.add(proxy)

if __name__ == '__main__':
    proxy_getter = IPProxyGetter()
    proxy_getter.run()