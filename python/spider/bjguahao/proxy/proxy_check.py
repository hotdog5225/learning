import asyncio

from proxy_redis import ProxyRedis

import aiohttp
import logging
import time

VALID_STATUS_CODE = [200]
TEST_URL = 'https://www.baidu.com'
BATCH_TEST_SIZE = 100

# logging.basicConfig(filename='./proxy_checker.log',
#                     filemode='a',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S',
#                     level=logging.DEBUG)


class ProxyChecker:
    def __init__(self):
        self.redis = ProxyRedis()

    async def test_single_proxy(self, str_proxy):
        '''
        测试单个代理
        '''
        conn = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(str_proxy, bytes):
                    str_proxy = str_proxy.decode('utf-8')
                real_proxy = 'https://' + str_proxy
                logging.info("正在测试proxy: %s", str_proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    print('checking....')
                    if response.status_code in VALID_STATUS_CODE:
                        logging.info("proxy ok")
                        self.redis.max(str_proxy)
                    else:
                        logging.info("proxy failed")
                        self.redis.decrease(str_proxy)
            except Exception as e:
                self.redis.decrease(str_proxy)

    def run(self):
        '''
        主函数
        '''
        logging.info("代理测试器开始运行")
        try:
            all_proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            # 批量测试
            for i in range(0, len(all_proxies), BATCH_TEST_SIZE):
                # 取一批待测试的proxy
                test_proxies = all_proxies[i: i+BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            logging.error(e)

if __name__ == '__main__':
    checker = ProxyChecker()
    checker.run()