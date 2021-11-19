import json
import logging
import os
import time
from datetime import datetime
import logging

import requests

from login.login import Login
from verify_code.verify_code import BaiduVerifyCode
from register.Register import Register
from register_Info.order import Order
from conf.config import PersonConfig
from conf.config import RegistorInfo
from crypt.my_crypto import Encryptor
from do.hospital_info import HospitalInfo
from do.department_info import DepartmentInfo
from request_info.header_info import HeaderInfo
from request_info.cookie_info import CookieInfo
from request_info.session_info import SessionInfo
from common.error_no import ErrorNum
from verify_code.secret import Secret
from font_decrypt.font_decrypt import FontDecryptor

from my_crawler.Crawler import BJGuaHaoCrawler

from bs4 import BeautifulSoup
import bs4.element

from storage.redis import RedisClient

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.INFO)

    # 判断cookie是否有效

    # dependencies
    error_num = ErrorNum()

    db_hospital_info = HospitalInfo()  # 医院db信息
    db_dept_info = DepartmentInfo()  # 诊室db信息

    person_info = PersonConfig()  # 配置信息
    register_info = RegistorInfo()  # 挂号信息

    redis = RedisClient().get_client()  # redis
    encryptor = Encryptor()  # 加密模块
    secret_info = Secret()
    baiduOCR = BaiduVerifyCode(secret_info, error_num)  # ocr
    login = Login(encryptor, error_num, baiduOCR, redis)  # login

    header_info = HeaderInfo()
    cookie_info = CookieInfo()
    session_info = SessionInfo(header_info, cookie_info, redis, error_num)  # session
    session_request, code = session_info.get_session_with_cookie()

    # font 解密
    font_decryptor = FontDecryptor(redis)
    # code = font_decryptor.get_code("//img.114yygh.com/fe/home/iconfont/c81e728d9d4c2f636f067f89cc14862c","&#xf594;&#xf62b;")

    if code != error_num.OK:
        # login and update cookie
        # get captcha code
        login.get_captcha_code(session_request)
        # recognize captcha code
        code = login.recognize_code(session_request)
        # validate captcha code
        login.check_code(session_request, code)
        # get sms code
        try:
            login.get_sms_code(session_request, code, person_info.phone_num)
        except Exception as e:
            print(e)
        # read sms msg code from db
        sms_code = input("输入手机验证码: ")
        time.sleep(2)
        login.login(session_request, person_info.phone_num, sms_code)

        # validate cookie
        is_valid = session_info.validate_cookie(session_request)
        if is_valid:
            logging.info(">>>> 用户登录成功!")
        else:
            logging.error(">>>> 用户登录失败!")
            exit()

    # print register info
    hosp_name = register_info.hospital_name
    dept_second_name = register_info.dept_second_name
    basic_info_dict = db_hospital_info.get_basic_info(hosp_name, dept_second_name)
    firstDeptCode = basic_info_dict['code']
    secondDeptCode = basic_info_dict['code2']
    hosCode = basic_info_dict['hosp_id']
    dept_first_name = basic_info_dict['dept_first_name']
    print(
        "待挂科室基础信息: {}({}), {}({}), {}({})".format(hosp_name, hosCode, dept_first_name, firstDeptCode, dept_second_name,
                                                  secondDeptCode))

    register = Register(
        firstDeptCode=firstDeptCode,
        secondDeptCode=secondDeptCode,
        hosCode=hosCode,
        session=session_request,
    )
    availabel_days = register.get_availabe_days()
    if len(availabel_days) == 0:
        logging.warning("\n>>>>>>> 当前没有可预约日期")


    exit()


