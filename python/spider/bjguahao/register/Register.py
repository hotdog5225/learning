import logging
import time
from datetime import datetime


# 挂号类
class Register:
    def __init__(self, **kwargs):
        valid_keys = [
            'hosCode',
            'firstDeptCode',
            'secondDeptCode',
            'target',
            'treatmentDay',
            'uniqProductKey',
            'dutyTime',
            'cardType',  # fixed
            'cardNo',  # fixed
            'hospitalCardId',  # fixed
            'phone',  # fixed
            'orderFrom',  # fixed
            'session',
        ]
        for key in valid_keys:
            setattr(self, key, kwargs.get(key))
        return

    def get_availabe_days(self):
        # get dept time list page
        data_dict = {
            "firstDeptCode": self.firstDeptCode,  # 诊室code1
            "secondDeptCode": self.secondDeptCode,  # 诊室code2
            "hosCode": self.hosCode,  # 医院编号
            "week": 1 # fixed
        }
        str_time = str(int(time.time()) * 1000 + 367)
        url = 'https://www.114yygh.com/web/product/list?_time=' + str_time
        response = self.session.post(url, json=data_dict)
        if response.status_code != 200:
            logging.error("[Register-get_available_days] http failed!")
            raise ValueError("[Register-get_available_days] http failed!")
        with open('dept_time_list.json', 'w') as f:
            f.write(response.content.decode('utf-8'))
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

    # 确认订单, 获取订单号
    def comfirm(self):
        # {
        #     "hosCode": "H14152001",
        #     "firstDeptCode": "hyde_EBH_c7d1eb9d_vir",
        #     "secondDeptCode": "BH",
        #     "target": "2021-11-08",
        #     "uniqProductKey": "2bb107ad6eb06bc235d6adce4baa067df95cb675",
        #     "dutyTime": "202111081330-202111081400"
        # }
        return

    # 下单
    def save(self):
        # {
        #     "hosCode": "H14152001",
        #     "firstDeptCode": "hyde_EBH_c7d1eb9d_vir",
        #     "secondDeptCode": "BH",
        #     "dutyTime": "202111081330-202111081400",
        #     "treatmentDay": "2021-11-08",
        #     "uniqProductKey": "2bb107ad6eb06bc235d6adce4baa067df95cb675",
        #     "cardType": "SOCIAL_SECURITY",
        #     "cardNo": "12074208401X",
        #     "smsCode": "",
        #     "hospitalCardId": "",
        #     "phone": "16601126121",
        #     "orderFrom": "HOSP"
        # }
        return
