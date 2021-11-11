import time
import random
import sys

import requests
from aip import AipOcr

from verify_code.secret import Secret

def get_random_agent():
    agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36 OPR/63.0.3368.43',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/534.54.16 (KHTML, like Gecko) Version/5.1.4 Safari/534.54.16',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3722.400 QQBrowser/10.5.3739.400',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 QIHU 360EE',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Safari/537.36']
    return agent_list[random.randint(0, 11)]


def get_random_refer():
    refer_list = [
        'https://www.114yygh.com/hospital/162/d4a80dff4262f5815eee0362515986cf/200052524/source',
    ]


def get_headers():
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'Accept': 'application/json, text/plain, */*',
        'Request-Source': 'PC',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': get_random_agent(),
        'Content-Type': 'application/json;charset=UTF-8',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.114yygh.com/hospital/162/d4a80dff4262f5815eee0362515986cf/200052524/source',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'x-tt-env': 'boe_dpa_i18n_creative_platform',
        'Host': 'www.114yygh.com'
    }
    return headers


def get_client():
    sys.path.append(".")
    s = Secret()
    app_id = s.app_id
    api_key = s.api_key
    secret_key = s.secret_key
    return AipOcr(app_id, api_key, secret_key)


# https://cloud.baidu.com/doc/OCR/s/7kibizyfm#%E7%BD%91%E7%BB%9C%E5%9B%BE%E7%89%87%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB
class BaiduVerifyCode:
    def __init__(self):
        self.client = get_client()

    """ 读取图片 """

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def virify_code(self):

        path = './captcha_code.jpg'
        image = self.get_file_content(path)

        """ 如果有可选参数 """
        options = {}
        options["detect_direction"] = "true"
        options["detect_language"] = "true"

        """ 带参数调用网络图片文字识别, 图片参数为本地图片 """
        try:
            result = self.client.webImage(image, options)
        except Exception as e:
            print(e)
            exit()

        print(result['words_result'][0]['words'])
        return result['words_result'][0]['words']


if __name__ == "__main__":
    baiduOCR = BaiduVerifyCode()
    baiduOCR.virify_code()
    pass
