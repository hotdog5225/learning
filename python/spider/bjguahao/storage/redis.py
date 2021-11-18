import redis

class RedisClient:
    def __init__(self):
        try:
            self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        except Exception as e:
            print(e)

    def get_client(self):
        return self.redis_client
