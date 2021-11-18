import time


class Order:
    def getOrders(self, session, persernal_config):
        # to set cookie: anti-spider
        post_data = {
            "keys": [
                "ORDER_STATUS"
            ]
        }
        str_time = str(int(time.time()) * 1000)
        url = 'https://www.114yygh.com/web/common/enum?_time={}'.format(str_time)
        session.post(url, data=post_data, verify=False)

        # to set cookie: anti-spider
        url = 'https://www.114yygh.com/web/patient/list?_time={}&showType=USER_CENTER'.format(str_time)
        session.get(url, verify=False)

        # get order
        str_time = str(int(time.time()) * 1000)
        url = 'https://www.114yygh.com/web/order/list?_time={}&idCardType=IDENTITY_CARD&idCardNo={}&orderStatus=ALL&pageNo=1&pageSize=10'.format(
            str_time, persernal_config.id_card)
        res = session.get(url, verify=False)
        with open('order_info.json', 'w') as f:
            f.write(res.content.decode('utf-8'))

