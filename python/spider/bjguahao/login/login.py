import json
import time

from crypt.my_crypto import Encryptor

class Login:
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
        print(response.content.decode('utf-8'))
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
        MyEncrypo = Encryptor()
        encrypt_phone_num = MyEncrypo.encrypt(phone_num)
        encrypt_sms_code = MyEncrypo.encrypt(sms_code)
        login_data = {
            "mobile": encrypt_phone_num,
            "code": encrypt_sms_code,
        }
        try:
            response = session.post(url, data=login_data)
            if response.status_code != 200:
                print(response.content.decode('utf-8'))
        except Exception as e:
            print(e)
