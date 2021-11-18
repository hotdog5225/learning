import mysql.connector
from mysql.connector import Error
from mysql.connector import connect, Error

import json


class HospitalInfo:
    def write_hospital_info_to_db(self, hospital_info_list):
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
                                  (info_dict['name'], info_dict['code'], info_dict['levelText'],
                                   info_dict['openTimeText']))
                    connection.commit()
                except:
                    connection.rollback()

    def dump_hospital_info(self):
        with open('./conf/hospital_info.json', 'r') as f:
            hospital_info_dict = json.loads(f.read())
            self.write_hospital_info_to_db(hospital_info_dict['data']['list'])
        print("DONE: hospital info dumped")

    def get_basic_info(self, hosp_name, dept_second_name):
        hosp_sql = "select name, hosp_id from hospital where name = '{}'".format(hosp_name)
        dept_sql = "select name, second_name, dept_code_1, dept_code_2 from department where second_name = '{}'".format(
            dept_second_name)
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
