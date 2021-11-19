import logging
import time
from datetime import datetime
import json


# 挂号类
class Register:
    def __init__(self, **kwargs):
        valid_keys = [
            'hosCode',
            'firstDeptCode',
            'secondDeptCode',
            'target',
            'session',
            'font_decrypter',
            'person_info',

            'treatmentDay',
            'uniqProductKey',
            'dutyTime',
            'cardType',  # fixed
            'cardNo',  # fixed
            'hospitalCardId',  # fixed
            'orderFrom',  # fixed
        ]
        for key in valid_keys:
            setattr(self, key, kwargs.get(key))

        self.register_info = {}
        return

    def get_availabe_days(self):
        # get dept time list page
        data_dict = {
            "firstDeptCode": self.firstDeptCode,  # 诊室code1
            "secondDeptCode": self.secondDeptCode,  # 诊室code2
            "hosCode": self.hosCode,  # 医院编号
            "week": 1  # fixed
        }
        str_time = str(int(time.time()) * 1000 + 367)
        url = 'https://www.114yygh.com/web/product/list?_time=' + str_time
        response = self.session.post(url, json=data_dict)
        if response.status_code != 200:
            logging.error("[Register-get_available_days] http failed!")
            raise ValueError("[Register-get_available_days] http failed!")
        # with open('dept_time_list.json', 'w') as f:
        #     f.write(response.content.decode('utf-8'))
        resp_data_dict = response.json()
        if resp_data_dict['resCode'] != 0:
            logging.error("[Register-get_available_days] failed, msg:{}".format(resp_data_dict['msg']))
            raise ValueError(resp_data_dict['msg'])
        next_appoint_time = datetime.fromtimestamp(resp_data_dict['data']['fhTimestamp'] / 1000)
        next_appoint_time_formatted = datetime.strptime(str(next_appoint_time), '%Y-%m-%d %H:%M:%S')
        print('下次放号时间: {}'.format(next_appoint_time_formatted))

        # get available days
        available_days = []
        target = ''
        calendars = resp_data_dict['data']['calendars']
        for singleday in calendars:
            status = singleday['status']
            # AVAILABLE: 有号
            # SOLD_OUT: 约满
            # NO_INVENTORY: 无号
            # TOMORROW_OPEN: 即将放号
            if status == 'AVAILABLE':
                available_days.append(singleday)

                target = singleday['dutyDate']  # 2021-11-11
                week_desc = singleday['weekDesc']  # 周日
                print('{}({})is available'.format(singleday['weekDesc'], singleday['dutyDate']))

        return available_days

    def get_specific_day_info(self, target_day):
        logging.info(">>>>>>>>>>>> 获取target_day的信息")
        str_time = str(int(time.time()) * 1000 + 23)
        url = "https://www.114yygh.com/web/product/detail?_time={}".format(str_time)
        data_dict = {
            "firstDeptCode": self.firstDeptCode,
            "secondDeptCode": self.secondDeptCode,
            "hosCode": self.hosCode,
            "target": target_day,
        }
        resp = self.session.post(url, json=data_dict, verify=False)
        if resp.status_code != 200:
            logging.error("[Register-get_specific_day_info] http failed!")
            raise ValueError("[Register-get_specific_day_info] http failed!")
        # with open('specific_day_info.json', 'w') as f:
        #     f.write(resp.content.decode('utf-8'))

        # 上下午, 这里默认上午
        resp_dict = resp.json()
        morning_info = resp_dict['data'][0]
        morning_font_img_url = morning_info['dutyImgUrl']
        # 具体到医生
        morning_info_doctor_detail = morning_info['detail'][-1]
        register_info = {
            "uniqProductKey": morning_info_doctor_detail["uniqProductKey"],
            "doctorName": morning_info_doctor_detail["doctorName"],
            "doctorTitleName": morning_info_doctor_detail["doctorTitleName"],
            "skill": morning_info_doctor_detail["skill"],
            "period": morning_info_doctor_detail["period"],
            "fcode": self.font_decrypter.get_code(morning_font_img_url, morning_info_doctor_detail["fcode"]),
            "ncode": self.font_decrypter.get_code(morning_font_img_url, morning_info_doctor_detail["ncode"]),
            "wnumber": morning_info_doctor_detail["wnumber"],
            "znumber": morning_info_doctor_detail["znumber"],
        }
        self.register_info = register_info
        logging.info("医生({}) 职级({}) 剩余({}) 价位({})".format(register_info['doctorName'], register_info['doctorTitleName'],
                                                          register_info['ncode'], register_info['fcode']))

    # 确认挂号信息
    def comfirm_order_info(self, target_day):

        logging.info(">>>>>>>>>>>>>>>>>> 第一次确认订单")
        str_time = str(int(time.time()) * 1000 + 367)
        url = 'https://www.114yygh.com/web/product/confirm?_time={}'.format(str_time)
        data_dict = {
            "hosCode": self.hosCode,
            "firstDeptCode": self.firstDeptCode,
            "secondDeptCode": self.secondDeptCode,
            "target": target_day,
            "uniqProductKey": self.register_info['uniqProductKey'],
            "dutyTime": "0"
        }
        resp = self.session.post(url, json=data_dict, verify=False)
        if resp.status_code != 200:
            logging.error("[register-confirm_order_info] http failed!")
            raise ValueError("[register-confirm_order_info] http failed!")

        # 获取验证码
        logging.info(">>>>>>>>>>>>>>>>>> 获取验证码")
        str_time = str(int(time.time()) * 1000 + 367)
        url = 'https://www.114yygh.com/web/common/verify-code/get?'
        query_dict = {
            '_time': str_time,
            'mobile': self.person_info.phone_num,
            'smsKey': "ORDER_CODE",
            'uniqProductKey': self.register_info['uniqProductKey'],
            'code': "",
        }
        resp = self.session.get(url, params=query_dict, verify=False)
        if resp.status_code != 200:
            logging.error("[register-confirm_order_info] http failed!")
            raise ValueError("[register-confirm_order_info] http failed!")

        sms_code = input("输入手机验证码: ")

        # 确认订单
        logging.info(">>>>>>>>>>>>>>>>>> 确认订单")
        str_time = str(int(time.time()) * 1000 + 367)
        url = 'https://www.114yygh.com/web/order/save?_time={}'.format(str_time)
        data_dict = {
            "hosCode": self.hosCode,
            "firstDeptCode": self.firstDeptCode,
            "secondDeptCode": self.secondDeptCode,
            "dutyTime": 0,
            "treatmentDay": target_day,
            "uniqProductKey": self.register_info['uniqProductKey'],
            "cardType": "SOCIAL_SECURITY",
            "cardNo": self.person_info.social_card_no,
            "smsCode": sms_code,
            "hospitalCardId": "",
            "phone": self.person_info.phone_num,
            "orderFrom": "HOSP"
        }
        resp = self.session.post(url, json=data_dict, verify=False)
        if resp.status_code != 200:
            logging.error("[register-confirm_order_info] http failed!")
            raise ValueError("[register-confirm_order_info] http failed!")

        resp_data_dict = resp.json()
        if resp_data_dict['resCode'] != 0:
            logging.error("[Register-confirm_order_info] failed, msg:{}".format(resp_data_dict['msg']))
            raise ValueError(resp_data_dict['msg'])

        order_no = resp_data_dict['data']['orderNo']
        self.register_info['orderNo'] = order_no

        return order_no


    def get_order_detail(self):
        logging.info(">>>>>>>>>>>>>> 获取订单详情")
        str_time = str(int(time.time()) * 1000 + 367)
        url = 'https://www.114yygh.com/web/order/detail?_time={}&hosCode={}&orderNo={}'.format(
            str_time,
            self.hosCode,
            self.register_info['orderNo'],
        )

        resp = self.session.get(url, verify=False)
        if resp.status_code != 200:
            logging.error("[register-get_order_detail] http failed!")
            raise ValueError("[register-get_order_detail] http failed!")

        with open('order_info.json', 'w') as f:
            f.write(resp.content.decode('utf-8'))

    def cacel_order(self, order_no, hosp_no):
        str_time = str(int(time.time()) * 1000 + 367)
        url = 'https://www.114yygh.com/web/order/cancel?_time={}&orderNo={}&hosCode={}'.format(
            str_time,
            order_no,
            hosp_no
        )
        resp = self.session.get(url, verify=False)
        if resp.status_code != 200:
            logging.error("[register-cancel_order] http failed!")
            raise ValueError("[register-cancel_order] http failed!")
        pass
