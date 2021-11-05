import json
import re
import sqlite3
import time

import my_crawler.Crawler

import requests
from requests_html import HTMLSession

from bs4 import BeautifulSoup
import bs4.element

import pandas as pd

import mysql.connector
from mysql.connector import Error
from mysql.connector import connect, Error

from datetime import datetime


# Q: 图片验证码识别, 触发验证码下发, 获取短信验证码, 登录

# datetime related
# https://www.programiz.com/python-programming/datetime/timestamp-datetime

# mysql
# https://realpython.com/python-mysql/

# determine whether response has data
# https://stackoverflow.com/questions/37605278/how-to-determine-if-my-python-requests-call-to-api-returns-no-data/37605377
# requests with bs4, selenium
# https://stackoverflow.com/questions/32937590/how-to-fake-javascript-enabled-in-python-requests-beautifulsoup

# scraping data from a javascript website
# http://theautomatic.net/2019/01/19/scraping-data-from-javascript-webpage-python/
# https://pypi.org/project/requests-html/

def getOTP():
    # connect with chat.db
    conn = sqlite3.connect("/Users/wuzewei.wzw/Library/Messages/chat.db")
    # get message and sender's info
    messages = pd.read_sql_query("select * from message order by ROWID desc limit 1", conn)
    handles = pd.read_sql_query("select * from handle order by ROWID desc limit 1", conn)

    # merge message and sender's info
    messages.rename(columns={'ROWID': 'message_id'}, inplace=True)
    handles.rename(columns={'id': 'phone_number', 'ROWID': 'handle_id'}, inplace=True)
    imessage_df = pd.merge(messages[['text', 'handle_id', 'date', 'is_sent', 'message_id']],
                           handles[['handle_id', 'phone_number']], on='handle_id', how='left')

    # print message text we expected
    re_code_pattern = re.compile(r'您的短信验证码为【(\d{6})】')
    for index, row in imessage_df.iterrows():
        match_code = re.search(re_code_pattern, row['text'], flags=0)
        print("Msg Code: ", match_code.group(1))
        return match_code


def get_cookie():
    # get cookie manually
    # TODO set cookie manually
    origin_cookie_str = 'imed_session=uQwGnhs9ZszCqfx0mhhv8q4RTFviqcyx_5453578; imed_session=uQwGnhs9ZszCqfx0mhhv8q4RTFviqcyx_5453578; SECKEY_CID=b496fb8f52209250ddcd517d438902a36a8c4303; BMAP_SECKEY=68929e83979a78fd015ed358fefc384ad77c1b324b8cc6f266f2a8ebe521879133a4ab1c7df9cb3c91dfbc5248943b06f8c7b7cc20a008330338202950984db93c6852080a710ea0d08a93346b9c9c52165a6912f3345de65fe7563a8123b57548c033076d5704b3bf186cfcfe38c610677784dbb502d56d78e6ef7dab5b1eb01c24f574b4b4a436134bf66192b1baa3b5b6c9705bc1c8d8536873338733f63aa5f07f2164f9cd25185c385ade0fcf2b21b648c743518f165e46c69a0b50b697ead084111812bf2d2a9e00cec732fef33bb3d7db183f55fce53bff96f350b84fab7318c0056d9ee8d947e2ca9a105b36; secure-key=f1d291ec-1370-4bd1-aaba-c71aab40bd45; imed_session=uQwGnhs9ZszCqfx0mhhv8q4RTFviqcyx_5453578; cmi-user-ticket=5OZgXINKlUNGpVg_MK_Tsxm_WghKtaLWMz8WZg..; agent_login_img_code=6777c8a2b65b46db85c2e232a077d1c9; imed_session_tm=1636073852950'
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
    hosp_sql = "select * from hospital where name = '{}'".format(hosp_name)
    dept_sql = "select * from department where second_name = '{}'".format(dept_second_name)
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
            'hosp_id': hosp_record_tuple[2],
            'code': dept_record_tuple[4],
            'code2': dept_record_tuple[5],
        }


if __name__ == '__main__':
    # write hospital info to db
    # dump_hospital_info()
    # exit()

    # write specific departments info to db
    # dump_department_info()
    # exit()

    hosp_name = '北京大学第三医院'
    dept_second_name = '肛肠门诊'
    basic_info_dict = get_basic_info(hosp_name, dept_second_name)
    # dict = {
    #     'hosp_id': hosp_record_tuple[2],
    #     'code': dept_record_tuple[4],
    #     'code2': dept_record_tuple[5],
    # }
    firstDeptCode = basic_info_dict['code']
    secondDeptCode = basic_info_dict['code2']
    hosCode = basic_info_dict['hosp_id']
    print("诊室基础信息: 一级诊室code:{}, 二级诊室code:{}, 医院id:{}".format(firstDeptCode, secondDeptCode, hosCode))

    # TODO delete
    firstDeptCode ='hyde_EBH_c7d1eb9d_vir'
    secondDeptCode = 'BH'
    hosCode = 'H14152001'

    # get department register info
    # TODO: set cookie manually
    cookie_dict = get_cookie()

    # header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
        'Referer': 'https://www.114yygh.com/hospital/1/home',
        'Request-Source': 'PC'
    }

    str_time = str(time.time() * 1000)
    session = requests.Session()

    # get dept time list page
    data_json = {
        "firstDeptCode": firstDeptCode,  # 诊室code1
        "secondDeptCode": secondDeptCode,  # 诊室code2
        "hosCode": hosCode,  # 医院编号
        "week": 1
    }
    response = session.post('https://www.114yygh.com/web/product/list?_time=' + str_time, headers=headers,
                            cookies=cookie_dict, json=data_json)
    try:
        data_dict = response.json()
        if data_dict['resCode'] != 0:
            print(data_dict['msg'])
            exit()
    except Exception as e:
        print(e)
        exit()

    calendars = data_dict['data']['calendars']
    next_appoint_time = datetime.fromtimestamp(data_dict['data']['fhTimestamp'] / 1000)
    next_appoint_time_formated = datetime.strptime(str(next_appoint_time), '%Y-%m-%d %H:%M:%S')
    print('下次放号时间: {}'.format(next_appoint_time_formated))

    # 获取预约日期
    target = ''
    for singleday in calendars:
        status = singleday['status']
        # AVAILABLE: 有号
        # SOLD_OUT: 约满
        # NO_INVENTORY: 无号
        # TOMORROW_OPEN: 即将放号
        if status == 'AVAILABLE':
            target = singleday['dutyDate']
            print('{}({})is available'.format(singleday['weekDesc'], singleday['dutyDate']))

            # TODO choose which one to appoint
            # appoint specific target day
            # get dept detail on target date
            data_json = {
                "firstDeptCode": firstDeptCode,  # 诊室code1
                "secondDeptCode": secondDeptCode,  # 诊室code2
                "hosCode": hosCode,  # 医院编号
                "target": target # 挂号日期
            }
            response = session.post('https://www.114yygh.com/web/product/detail?_time=' + str_time, headers=headers,
                                    cookies=cookie_dict, json=data_json)
            print(json.loads(response.json()))
            exit()
