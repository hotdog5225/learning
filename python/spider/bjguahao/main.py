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


# mysql
# https://realpython.com/python-mysql/

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
    origin_cookie_str = 'imed_session=Yig8m6ncVuEszfx7CrcOxBRSDslXeEJd_5452914; secure-key=f2011fac-0460-43b6-a6e8-c0b2bc51a157; imed_session=Yig8m6ncVuEszfx7CrcOxBRSDslXeEJd_5452914; agent_login_img_code=dda88711404947eaa016e2a6c16ca459; cmi-user-ticket=KlOznR8x1J3kbI9Y0wHN3G_9j3GU7A01i41Cdw..; imed_session_tm=1635874442991'
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


if __name__ == '__main__':
    # write hospital info to db
    # dump_hospital_info()
    # exit()

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

    # hospital homepage
    url = "https://www.114yygh.com/web/department/hos/list?_time=" + str_time + "&hosCode=1"
    response = session.get(url=url, headers=headers, cookies=cookie_dict)

    # write hospital info to db
    hostpital_list = response.json['data']['list']

    print(response.json())
    exit()

    # get dept page
    response = session.get(url=url, headers=headers, cookies=cookie_dict)
    print(response.json())
    exit()

    # get dept time list page
    data_json = {
        "firstDeptCode": "02dd9e3ac47f03a72c7545960db87f84",  # 诊室code1
        "secondDeptCode": "200044340",  # 诊室code2
        "hosCode": "120",  # 医院编号
        "week": 1
    }
    response = session.post('https://www.114yygh.com/web/product/list?_time=' + str_time, headers=headers,
                            cookies=cookie_dict, json=data_json)

    data_dict = response.json()
    calendars = data_dict['data']['calendars']
    print(calendars)

    # 获取预约日期
    target = ''
    for singleday in calendars:
        status = singleday['status']
        if status == 'ENTORY' or status == 'AVAILABLE':
            target = singleday['dutyDate']
            print('%s is available', singleday['weekDesc'])

    # get dept detail on target date
    data_json = {
        "firstDeptCode": "02dd9e3ac47f03a72c7545960db87f84",
        "secondDeptCode": "200044340",
        "hosCode": "120",
        "target": target
    }
    response = session.post('https://www.114yygh.com/web/product/detail?_time=' + str_time, headers=headers,
                            cookies=cookie_dict, json=data_json)
    print(response.json())
