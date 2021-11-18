import json
import time
import logging
import pprint
from pprint import pformat
import requests

import requests

class SessionInfo:
    def __init__(self, header_info, cookie_info, redis, err_no):
        self.header_info = header_info
        self.cookie_info = cookie_info
        self.redis = redis
        self.err_no = err_no

    def get_session_with_cookie(self):
        headers = self.header_info.getGeneralHeader()

        session = requests.Session()
        session.headers = headers

        is_valid = self.validate_cookie(session)
        if not is_valid:
            return session, self.err_no.USER_NOT_LOGIN
        else:
            return session, self.err_no.OK

    def validate_cookie(self, session):
        str_time = str(int(time.time()) * 1000)
        cookie_key = '114_login_cookie'
        str_cookie = self.redis.get(cookie_key)

        # cookie_dict = {}
        # cookie_list = str_cookie.split('; ')
        # for cookie in cookie_list:
        #     cookie_dict[cookie.split('=')[0]] = cookie.split('=')[1]

        cookie_dict = json.loads(str_cookie)

        logging.info('current cookie is: %s', json.dumps(cookie_dict))

        # set cookie to session
        for key, value in cookie_dict.items():
            cookie = requests.cookies.create_cookie(key, value)
            session.cookies.set_cookie(cookie)

        url = 'https://www.114yygh.com/web/patient/list?_time={}&showType=USER_CENTER'.format(str_time)
        resp = session.get(url)

        if resp.status_code != 200:
            logging.error("[session_info - validate_cookie] http failed!")
            raise ValueError("[session_info - validate_cookie] http failed!")

        resp_dict = json.loads(resp.content.decode('utf-8'))
        if resp_dict['resCode'] != 0:
            logging.error(resp_dict['msg'])
            return False

        return True
