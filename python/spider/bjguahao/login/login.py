import json
import time


class Login:
    def __init__(self, arg_encryptor):
        # 加密模块
        self.encryptor = arg_encryptor

    # get captcha pic
    def getCptcharCode(self, session):
        url = 'https://www.114yygh.com/web/img/getImgCode?_time={}'.format(str(int(time.time()) * 1000))
        response = session.get(url)
        with open('captcha_code.jpg', 'wb') as f:
            f.write(response.content)
            f.flush()

    # validate captcha pic
    def checkCode(self, session, code):
        str_time = str(int(time.time()) * 1000)
        url = 'https://www.114yygh.com/web/checkcode?_time={}&code={}'.format(str_time, code)
        response = session.get(url)
        print(response.request.headers)
        print(response.headers)
        res_dict = json.loads(response.content.decode('utf-8'))
        if res_dict['resCode'] != 0:
            print(res_dict['msg'])
            exit()

    # send SMS code
    def getSMSCode(self, session, code, phone_num):
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
