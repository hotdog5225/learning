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
        ]
        for key in valid_keys:
            setattr(self, key, kwargs.get(key))
        return

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
