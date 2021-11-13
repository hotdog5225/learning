import selenium.webdriver as wb
import http.cookiejar
import json
import random
import time

from login.login import Login
from verify_code.verify_code import BaiduVerifyCode
from message.message import Message

from my_crawler.Crawler import BJGuaHaoCrawler

import requests
from requests_html import HTMLSession

from bs4 import BeautifulSoup
import bs4.element

import mysql.connector
from mysql.connector import Error
from mysql.connector import connect, Error

from datetime import datetime

from conf.config import PersonConfig
from conf.config import RegistorInfo

def get_cookie():
    # get cookie manually
    # TODO set cookie manually
    origin_cookie_str = 'imed_session=0nE81eZWGlDT5O9cz0NAzbAkarlgYzR1_5453766; imed_session=0nE81eZWGlDT5O9cz0NAzbAkarlgYzR1_5453766; imed_session=Ifaqx1G2qYL7U9PIEH8OqlJtHMLx3UvG_5453756; SECKEY_CID=b496fb8f52209250ddcd517d438902a36a8c4303; BMAP_SECKEY=68929e83979a78fd015ed358fefc384ad77c1b324b8cc6f266f2a8ebe521879133a4ab1c7df9cb3c91dfbc5248943b06f8c7b7cc20a008330338202950984db93c6852080a710ea0d08a93346b9c9c52165a6912f3345de65fe7563a8123b57548c033076d5704b3bf186cfcfe38c610677784dbb502d56d78e6ef7dab5b1eb01c24f574b4b4a436134bf66192b1baa3b5b6c9705bc1c8d8536873338733f63aa5f07f2164f9cd25185c385ade0fcf2b21b648c743518f165e46c69a0b50b697ead084111812bf2d2a9e00cec732fef33bb3d7db183f55fce53bff96f350b84fab7318c0056d9ee8d947e2ca9a105b36; cmi-user-ticket=tiWrDsSsNgxzQ_Ud3_ySP2Vs928sR44bBjVJdg..; secure-key=bba4311a-61d2-406c-99fc-5e25c7b7aa59; agent_login_img_code=7dc7ab1cf1dd4f29841f6e2b4de86dcf; imed_session=CL0BU6jZOyLg4j97NCOYksigCBZPDTBI_5453770; imed_session_tm={}' \
        .format(str(int(time.time()) * 1000))
    cookie_dict = {}
    cookie_list = origin_cookie_str.split('; ')
    for cookie in cookie_list:
        cookie_dict[cookie.split('=')[0]] = cookie.split('=')[1]

    return cookie_dict


def write_hospital_info_to_db(hospital_info_list):
    insert_sql = '''
    INSERT INTO hospital
        ( name, hosp_id, level, open_text)
    VALUES
       (%s, %s, %s, %s)
    '''
    with connect(
            host="localhost",
            user='root',
            password='rootroot',
            database="bjguahao",
    ) as connection:
        cusor = connection.cursor()
        for info_dict in hospital_info_list:
            """
            { 
                "code":"162",
                "name":"中国人民解放军总医院(301医院)",
                "picture":"//img.114yygh.com/image/image-003/23177271556061774.png",
                "levelText":"三级甲等",
                "openTimeText":"08:30",
                "maintain":false,
                "distance":null
            },
            """
            try:
                cusor.execute(insert_sql,
                              (info_dict['name'], info_dict['code'], info_dict['levelText'], info_dict['openTimeText']))
                connection.commit()
            except:
                connection.rollback()


def dump_hospital_info():
    with open('./conf/hospital_info.json', 'r') as f:
        hospital_info_dict = json.loads(f.read())
        write_hospital_info_to_db(hospital_info_dict['data']['list'])
    print("DONE: hospital info dumped")


def write_department_info_to_db(department_info_list, hosp_id):
    insert_sql = """
    insert into department (name, second_name, hosp_id, dept_code_1, dept_code_2, hot_dept) VALUES (%s, %s, %s, %s, %s, %s);
    """
    with connect(
            host="localhost",
            user='root',
            password='rootroot',
            database="bjguahao",
    ) as connection:
        cusor = connection.cursor()
        for info_dict in department_info_list:
            """
             {
                "code":"f689f7f4889e1924c0747cdfb5db8ace",
                "name":"老年医学科门诊",
                "subList":[
                    {
                        "code":"200053329",
                        "name":"老年医学科门诊",
                        "dept1Code":"f689f7f4889e1924c0747cdfb5db8ace",
                        "hotDept":false
                    },
                    {
                        "code":"200053329",
                        "name":"老年医学科门诊",
                        "dept1Code":"f689f7f4889e1924c0747cdfb5db8ace",
                        "hotDept":false
                    }
                ]
            },
            """
            name = info_dict['name']
            code1 = info_dict['code']
            for second_info_dict in info_dict['subList']:
                code2 = second_info_dict['code']
                second_name = second_info_dict['name']
                hot_dept = second_info_dict['hotDept']
                try:
                    cusor.execute(insert_sql,
                                  (name, second_name, hosp_id, code1, code2, hot_dept)
                                  )
                    connection.commit()
                except Exception as e:
                    print(e)
                    connection.rollback()


def dump_department_info():
    # XieHe_hosp_id = 1
    # with open('./conf/XieHe_dept_info.json', 'r') as f:
    #     department_info_dict = json.loads(f.read())
    #     write_department_info_to_db(department_info_dict['data']['list'][1:], XieHe_hosp_id)

    BeiYiSanYuan_hosp_id = 142
    with open('./conf/BeiYiSanYuan_dept_info.json', 'r') as f:
        department_info_dict = json.loads(f.read())
        write_department_info_to_db(department_info_dict['data']['list'][1:], BeiYiSanYuan_hosp_id)
    print("DONE: department info dumped")


def get_basic_info(hosp_name, dept_second_name):
    hosp_sql = "select name, hosp_id from hospital where name = '{}'".format(hosp_name)
    dept_sql = "select name, second_name, dept_code_1, dept_code_2 from department where second_name = '{}'".format(dept_second_name)
    with connect(
            host="localhost",
            user='root',
            password='rootroot',
            database="bjguahao",
    ) as connection:
        cusor = connection.cursor()
        # hospital info
        cusor.execute(hosp_sql)
        hosp_record_tuple = cusor.fetchone()
        # dept info
        cusor.execute(dept_sql)
        dept_record_tuple = cusor.fetchone()

        return {
            'hosp_id': hosp_record_tuple[1],
            'dept_first_name': dept_record_tuple[0],
            'code': dept_record_tuple[2],
            'code2': dept_record_tuple[3],
        }


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


def get_session():
    # cookie_dict = get_cookie()
    # cookie_jar = http.cookiejar.CookieJar()
    headers = get_headers()

    session = requests.Session()
    session.headers = headers
    # session.cookies = requests.utils.add_dict_to_cookiejar(cookie_jar, cookie_dict)
    return session


if __name__ == '__main__':
    # write hospital info to db
    # dump_hospital_info()
    # exit()

    # write specific departments info to db
    # dump_department_info()
    # exit()

    # get basic info
    person_info = PersonConfig()
    register_info = RegistorInfo()
    phone_num = person_info.phone_num

    hosp_name = '北京大学第三医院'
    dept_second_name = '肛肠门诊'
    basic_info_dict = get_basic_info(hosp_name, dept_second_name)
    firstDeptCode = basic_info_dict['code']
    secondDeptCode = basic_info_dict['code2']
    hosCode = basic_info_dict['hosp_id']
    dept_first_name = basic_info_dict['dept_first_name']
    print("待挂科室基础信息: {}({}), {}({}), {}({})".format(hosp_name, hosCode, dept_first_name, firstDeptCode, dept_second_name,
                                              secondDeptCode))

    session_request = get_session()
    # set cookie by remote
    url = 'https://www.114yygh.com/web/img/getImgCode?_time={}'.format(str(int(time.time()) * 1000))
    session_request.get(url)

    # login
    # get captcha code
    login = Login()
    login.getCptcharCode(session_request)
    # recognize cpatcha code
    baiduOCR = BaiduVerifyCode()
    code = baiduOCR.virify_code()
    # validate captcha code
    login.checkCode(session_request, code)
    # get sms code
    login.getSMSCode(session_request, code, phone_num)
    # read sms msg code from db
    sms_code = input("sms code: ")
    login.login(session_request, phone_num, sms_code)
    # get registrr info for test
    str_time = str(int(time.time()) * 1000)
    url = 'https://www.114yygh.com/web/order/list?_time={}&idCardType=IDENTITY_CARD&idCardNo=320381199003150312&orderStatus=ALL&pageNo=1&pageSize=10'.format(str_time)
    res = session_request.get(url)
    with open('text.html', 'w') as f:
        f.write(res.content.decode('utf-8'))
    exit()

    # get department register info
    str_time = str(int(time.time()) * 1000)

    # get dept time list page
    data_dict = {
        "firstDeptCode": firstDeptCode,  # 诊室code1
        "secondDeptCode": secondDeptCode,  # 诊室code2
        "hosCode": hosCode,  # 医院编号
        "week": 1
    }
    url = 'https://www.114yygh.com/web/product/list?_time=' + str_time
    response = session_request.post(url, data=data_dict)
    try:
        resp_data_dict = response.json()
        if resp_data_dict['resCode'] != 0:
            print(resp_data_dict['msg'])
            exit()
    except Exception as e:
        print(e)
        exit()

    calendars = resp_data_dict['data']['calendars']
    next_appoint_time = datetime.fromtimestamp(resp_data_dict['data']['fhTimestamp'] / 1000)
    next_appoint_time_formated = datetime.strptime(str(next_appoint_time), '%Y-%m-%d %H:%M:%S')
    print('下次放号时间: {}'.format(next_appoint_time_formated))

    # check which day is available
    target = ''
    for singleday in calendars:
        status = singleday['status']
        # AVAILABLE: 有号
        # SOLD_OUT: 约满
        # NO_INVENTORY: 无号
        # TOMORROW_OPEN: 即将放号
        if status == 'AVAILABLE':
            target = singleday['dutyDate']  # 2021-11-11
            week_desc = singleday['weekDesc']  # 周日
            print('{}({})is available'.format(singleday['weekDesc'], singleday['dutyDate']))
            exit

            # TODO choose which day to appoint

            # appoint specific target day
            # page is rendered by javascript, use selenium
            url = "https://www.114yygh.com/hospital/{}/{}/{}/source".format(hosCode, firstDeptCode, secondDeptCode)
            bjGuaHaoCrawler = BJGuaHaoCrawler()
            dept_detail_html = bjGuaHaoCrawler.get_html_dept_detail(url, week_desc)

            # parse html
            soup = BeautifulSoup(dept_detail_html, "lxml")
            morning_num_remain_tag = soup.find('span', attrs={
                'style': 'font-family: magic_1;',
            })
            print(repr(morning_num_remain_tag.string))
            exit()
