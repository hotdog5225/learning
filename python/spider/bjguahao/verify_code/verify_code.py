import logging
import time
import random
import sys

import requests
from aip import AipOcr


# https://cloud.baidu.com/doc/OCR/s/7kibizyfm#%E7%BD%91%E7%BB%9C%E5%9B%BE%E7%89%87%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB
class BaiduVerifyCode:
    def __init__(self, secret, error_num):
        self.secret = secret
        self.client = self.get_client()
        self.error_num = error_num

    def get_client(self):
        sys.path.append(".")
        s = self.secret
        app_id = s.app_id
        api_key = s.api_key
        secret_key = s.secret_key
        return AipOcr(app_id, api_key, secret_key)

    """ 读取图片 """

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def recognize_code(self):
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

        if len(result['words_result'][0]['words']) == 0:
            logging.error("OCR failed, empty code")
            raise ValueError("OCR failed, empty code")

        # print("captcha_code is: ", result['words_result'][0]['words'])
        logging.info("captcha_code is: %s", str(result['words_result'][0]['words']))

        return result['words_result'][0]['words']


if __name__ == "__main__":
    baiduOCR = BaiduVerifyCode()
    baiduOCR.recognize_code()
    pass
