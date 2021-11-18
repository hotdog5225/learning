import mysql.connector
from mysql.connector import Error
from mysql.connector import connect, Error

import json

class DepartmentInfo:
    def write_department_info_to_db(self, department_info_list, hosp_id):
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

    def dump_department_info(self):
        # XieHe_hosp_id = 1
        # with open('./conf/XieHe_dept_info.json', 'r') as f:
        #     department_info_dict = json.loads(f.read())
        #     write_department_info_to_db(department_info_dict['data']['list'][1:], XieHe_hosp_id)

        BeiYiSanYuan_hosp_id = 142
        with open('./conf/BeiYiSanYuan_dept_info.json', 'r') as f:
            department_info_dict = json.loads(f.read())
            self.write_department_info_to_db(department_info_dict['data']['list'][1:], BeiYiSanYuan_hosp_id)
        print("DONE: department info dumped")