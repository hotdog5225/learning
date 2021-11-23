import logging
import sys

sys.path.append('../storage/')
from redis import Redis

from random import choice
import redis

MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
REDIS_SET_KEY = "proxies"


class ProxyRedis:
    '''
    提供redis存储接口
    '''

    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)

    def add(self, str_proxy, score=INITIAL_SCORE):
        '''
        添加代理,设置分数为最高:
        param proxy:代理:
        param Score:分数:
        return:添加结果
        '''
        if not self.redis.zscore(REDIS_SET_KEY, str_proxy):
            mapping = {
                str_proxy: score,
            }
            logging.info("add proxy %s", str_proxy)
            self.redis.zadd(REDIS_SET_KEY, mapping)

    def random(self):
        '''
        随机获取有效代理,首先尝试获取最高分数代理,如果最高分数不存在,则按照排名获取,否则异常
        return:随机代理
        '''
        result = self.redis.zrangebyscore(REDIS_SET_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.redis.zrevrange(REDIS_SET_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise ValueError("no proxy in pool!")

    def decrease(self, str_proxy):
        '''
        代理値减一分,分数小于最小值,则代理删除
        '''
        score = self.redis.zscore(REDIS_SET_KEY, str_proxy)
        if score and score > MIN_SCORE:
            logging.info('代理 %s 当前分数 %s 减1', str_proxy, score)
            return self.redis.zincrby(REDIS_SET_KEY, -1, str_proxy)
        else:
            logging.info('移除代理 %s', str_proxy)
            return self.redis.zrem(REDIS_SET_KEY, str_proxy)

    def exists(self, str_proxy):
        '''
        判断是否存在
        '''
        return not self.redis.zscore(REDIS_SET_KEY, str_proxy) == None

    def max(self, str_proxy):
        '''
        将代理的分数设置为最高
        '''
        logging.info('代理 %s 设置为最高分', str_proxy)
        return self.redis.zadd(REDIS_SET_KEY, MAX_SCORE, str_proxy)

    def count(self):
        """
        获取代理数量
        """
        return self.redis.zcard(REDIS_SET_KEY)

    def all(self):
        '''
        获取全部代理
        '''
        return self.redis.zrangebyscore(REDIS_SET_KEY, MIN_SCORE, MAX_SCORE)


if __name__ == '__main__':
    redis = Redis()
    redis.zscore()
