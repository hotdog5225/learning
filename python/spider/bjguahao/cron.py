import schedule
import time
import redis
import json
import logging
import requests
from storage.redis import RedisClient
from request_info.session_info import SessionInfo
from request_info.header_info import HeaderInfo
from request_info.cookie_info import CookieInfo
from common.error_no import ErrorNum


def validate_cookie():
    logging.basicConfig(filename="log_cookie_validation.txt",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    my_redis = RedisClient().get_client()  # redis

    str_time = str(int(time.time()) * 1000)
    cookie_key = '114_login_cookie'
    str_cookie = my_redis.get(cookie_key)

    cookie_dict = json.loads(str_cookie)

    logging.info('current cookie is: %s', json.dumps(cookie_dict))

    # set cookie to session
    header_info = HeaderInfo()
    cookie_info = CookieInfo()
    error_num = ErrorNum()
    session_info = SessionInfo(header_info, cookie_info, my_redis, error_num)  # session
    session, code = session_info.get_session_with_cookie()

    # validate cookie
    url = 'https://www.114yygh.com/web/patient/list?_time={}&showType=USER_CENTER'.format(str_time)
    resp = session.get(url)

    if resp.status_code != 200:
        logging.error("[session_info - validate_cookie] http failed!")

    resp_dict = json.loads(resp.content.decode('utf-8'))
    if resp_dict['resCode'] != 0:
        logging.error(resp_dict['msg'])
    else:
        logging.info("cookie有效!")


if __name__ == '__main__':
    schedule.every(2).minutes.do(validate_cookie)

    while True:
        schedule.run_pending()
        time.sleep(1)
