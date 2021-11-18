import json
import logging
import time

class Login:
    def __init__(self, arg_encryptor, error_num, ocr):
        # 加密模块
        self.encryptor = arg_encryptor
        self.error_num = error_num
        self.ocr = ocr

    # get captcha pic
    def get_captcha_code(self, session):
        url = 'https://www.114yygh.com/web/img/getImgCode?_time={}'.format(str(int(time.time()) * 1000))
        response = session.get(url)
        if response.status_code != 200:
            logging.error("get captcha_code error")
            return self.error_num.CALL_MODULE_ERROR
        with open('captcha_code.jpg', 'wb') as f:
            f.write(response.content)
            f.flush()

    # recognize captcha code
    def recognize_code(self):
        code, err_no = self.ocr.recognize_code()
        if err_no != 0 or len(code) != 4:
            time.sleep(0.2)
            self.get_captcha_code()
            self.recognize_code()
        else:
            return code

        return code

    # validate captcha pic
    def check_code(self, session, code):
        str_time = str(int(time.time()) * 1000)
        url = 'https://www.114yygh.com/web/checkcode?_time={}&code={}'.format(str_time, code)
        response = session.get(url)
        if response.status_code != 200:
            self.logging.error("check_code failed!")
            return self.error_num.CALL_MODULE_ERROR

        res_dict = json.loads(response.content.decode('utf-8'))
        if res_dict['resCode'] != 0:
            logging.error("check_code failed! msg: %s", res_dict['msg'])
            return self.error_num.CALL_MODULE_ERROR

        logging.info("validate captcha code ok!")

    # send SMS code
    def get_sms_code(self, session, code, phone_num):
        str_time = str(int(time.time()) * 1000)
        url = 'https://www.114yygh.com/web/common/verify-code/get?_time={}&mobile={}&smsKey=LOGIN&code={}'.format(
            str_time, phone_num, code)
        try:
            response = session.get(url)
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
        print(json.dumps(login_data))
        try:
            response = session.post(url, data=login_data, verify=False)
            print("response header:", response.headers)
            print("request header:", response.request.headers)
            with open('login_info.html', 'w') as f:
                f.write(response.content.decode('utf-8'))
        except Exception as e:
            print(e)
