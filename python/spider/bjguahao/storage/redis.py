import os

import time

import redis


class RedisClient:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        if not self.is_redis_available(self.redis_client):
            os.system("brew services start redis")
            time.sleep(1)
            self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

    def get_client(self):
        return self.redis_client

    def is_redis_available(self, r):
        try:
            r.ping()
            print("Successfully connected to redis")
        except (redis.exceptions.ConnectionError, ConnectionRefusedError):
            print("Redis connection error!")
            return False
        return True
