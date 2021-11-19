import json
import logging
import time


class Login:
    def __init__(self, arg_encryptor, error_num, ocr, redis):
        # 加密模块
        self.encryptor = arg_encryptor
        self.error_num = error_num
        self.ocr = ocr
        self.redis = redis

    # get captcha pic
    def get_captcha_code(self, session):
        url = 'https://www.114yygh.com/web/img/getImgCode?_time={}'.format(str(int(time.time()) * 1000))
        response = session.get(url)
        if response.status_code != 200:
            logging.error("get captcha_code error")
            raise ValueError("get captcha_code error")
        with open('captcha_code.jpg', 'wb') as f:
            f.write(response.content)
            f.flush()

    # recognize captcha code
    def recognize_code(self, session):
        code = ""
        try:
            code = self.ocr.recognize_code()
        except Exception as e:
            print(e)

        if len(code) != 4:
            time.sleep(2)
            self.get_captcha_code(session)
            self.recognize_code(session)

        return code

    # validate captcha pic
    def check_code(self, session, code):
        str_time = str(int(time.time()) * 1000 + 2000)
        url = 'https://www.114yygh.com/web/checkcode?_time={}&code={}'.format(str_time, code)
        response = session.get(url)
        if response.status_code != 200:
            self.logging.error("check_code failed!")
            raise ValueError("check_code failed!")

        with open("test.txt", "w") as f:
            f.write(response.content.decode('utf-8'))

        res_dict = json.loads(response.content.decode('utf-8'))
        if res_dict['resCode'] != 0:
            logging.error("check_code failed! msg: %s", res_dict['msg'])
            raise ValueError("check_code failed!")

        logging.info("validate captcha code ok!")

    # send SMS code
    def get_sms_code(self, session, code, phone_num):
        str_time = str(int(time.time()) * 1000)
        url = 'https://www.114yygh.com/web/common/verify-code/get?_time={}&mobile={}&smsKey=LOGIN&code={}'.format(
            str_time, phone_num, code)
        try:
            resp = session.get(url)
            if resp.status_code != 200:
                logging.error("[login-get_sms_code] failed!")
                raise ValueError("[login-get_sms_code] failed!")
        except Exception as e:
            print(e)
            exit()

    # login
    def login(self, session, phone_num, sms_code):
        str_time = str(int(time.time()) * 1000)
        url = "https://www.114yygh.com/web/login?_time={}".format(str_time)
        encrypt_phone_num = self.encryptor.encrypt(phone_num)
        encrypt_sms_code = self.encryptor.encrypt(sms_code)
        login_data = {
            "mobile": encrypt_phone_num,
            "code": encrypt_sms_code,
        }
        try:
            response = session.post(url, json=login_data, verify=False)
            if response.status_code != 200:
                logging.error("[login-login] login failed!")
                raise ValueError("[login-login] login failed!")

            # set cookie redis
            try:
                self.redis.set('114_login_cookie', json.dumps(session.cookies.get_dict()))
            except Exception as e:
                print(e)

        except Exception as e:
            print(e)
