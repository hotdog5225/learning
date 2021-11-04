import re
import sqlite3
import time

import bs4.element
import pandas as pd

from selenium import webdriver as wb
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from w3lib.html import remove_comments

from bs4 import BeautifulSoup

import requests

from requests_html import HTMLSession

import mysql.connector
from mysql.connector import Error

from getpass import getpass
from mysql.connector import connect, Error


# mysql
# https://realpython.com/python-mysql/

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


# requests with bs4, selenium
# https://stackoverflow.com/questions/32937590/how-to-fake-javascript-enabled-in-python-requests-beautifulsoup

# scraping data from a javascript website
# http://theautomatic.net/2019/01/19/scraping-data-from-javascript-webpage-python/
# https://pypi.org/project/requests-html/

def create_database(connection):
    try:
        create_db_query = "CREATE DATABASE hospital"
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)
    except Exception as e:
        print(e)


def get_cursor():
    # connet to mysql
    try:
        with connect(
                host="localhost",
                user='root',
                password='rootroot',
                database="bjguahao",
        ) as connection:
            pass
    except Error as e:
        print(e)

    cursor = connection.cursor()
    return cursor


def get_cookie():
    # get cookie manually
    origin_cookie_str = 'imed_session=Yig8m6ncVuEszfx7CrcOxBRSDslXeEJd_5452914; secure-key=f2011fac-0460-43b6-a6e8-c0b2bc51a157; imed_session=Yig8m6ncVuEszfx7CrcOxBRSDslXeEJd_5452914; agent_login_img_code=dda88711404947eaa016e2a6c16ca459; cmi-user-ticket=KlOznR8x1J3kbI9Y0wHN3G_9j3GU7A01i41Cdw..; imed_session_tm=1635874442991'
    cookie_dict = {}
    cookie_list = origin_cookie_str.split('; ')
    for cookie in cookie_list:
        cookie_dict[cookie.split('=')[0]] = cookie.split('=')[1]

    return cookie_dict


def get_hospital_info(html):
    with open('page_source.html', 'w') as f:
        f.write(html)
    soup = BeautifulSoup(html, features='lxml')
    hosp_item_tags = soup.find_all('div', attrs={
        'class': re.compile('hos-item')
    })

    for hosp_item_tag in hosp_item_tags:
        # get hospital name
        hospital_name_tag = hosp_item_tag.find('div', attrs={
            'class': 'hospital-title',
        })
        hospital_name = hospital_name_tag.contents[0].strip()
        # get hospital level
        tag_list = hosp_item_tag.find_all('div', attrs={
            'class': 'icon_wrapper'
        })
        hospital_level_tag = tag_list[0]
        level = ""
        for child in hospital_level_tag.contents:
            if isinstance(child, bs4.element.NavigableString):
                level = child.strip()
        # get hospital open time
        open_time_tag = tag_list[1]
        open_time = ""
        for child in open_time_tag.contents:
            if isinstance(child, bs4.element.NavigableString):
                open_time = re.search(r'\d.*\d', child.strip()).group()
        # print(hospital_name, " ", level, " ", open_time)

        # database 写入医院信息
        cursor = get_cursor()


if __name__ == '__main__':
    # 动态网页抓取
    driver = wb.Chrome()
    driver.get("https://www.114yygh.com/")
    # 初始有一个向导, 随便点击一个元素关掉
    driver.find_element(By.TAG_NAME, "body").click()
    # 滚动条拉到底部 js
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    # 页面下拉, 模拟按键page-down: 触发js执行
    bodyTag = driver.find_element(By.TAG_NAME, 'body')
    bodyTag.click()
    bodyTag.send_keys(Keys.PAGE_DOWN)

    # 确保某个元素存在(等待ajax加载完成)
    # 隐式等待
    try:
        driver.implicitly_wait(10)
        hosp_item_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'hos-item')]")
    except NoSuchElementException as e:
        print(e)
        exit()
    # 显示等待,10找不到就报错
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'hos-item')]")))

    # use bs4 to parse html
    html = driver.page_source
    get_hospital_info(html)

    # 退出driver
    driver.quit()

    exit()

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
