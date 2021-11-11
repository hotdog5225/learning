import json
import time
class Login:
    def getCptcharCode(self, session):
        url = 'https://www.114yygh.com/web/img/getImgCode?_time={}'.format(str(int(time.time()) * 1000))
        response = session.get(url)
        with open('captcha_code.jpg', 'wb') as f:
            f.write(response.content)
            f.flush()

    def checkCode(self, session, code):
        str_time = str(int(time.time())*1000)
        url = 'https://www.114yygh.com/web/checkcode?_time={}&code={}'.format(str_time, code)
        response = session.get(url)
        print(response.content.decode('utf-8'))
        res_dict = json.loads(response.content.decode('utf-8'))
        if res_dict['resCode'] != 0:
            print(res_dict['msg'])
            exit()

    def getSMSCode(self, session, code, phone_num):
        str_time = str(int(time.time())*1000)
        url = 'https://www.114yygh.com/web/common/verify-code/get?_time={}&mobile={}&smsKey=LOGIN&code={}'.format(str_time, phone_num, code)
        try:
            response = session.get(url)
        except Exception as e:
            print(e)
            exit()