import re

set_1 = set()
set_2 = set()
set_3 = set()
set_4 = set()
set_5 = set()
set_6 = set()
set_7 = set()

with open('metrics.log', 'r') as f:
    for line in f.readlines():
        number_list = line.split(';')
        checker_id = number_list[0]
        print(checker_id)
        if checker_id == ' - checker_id: 1':
            print(number_list[1])
            set_1.add(number_list[1])
        elif checker_id == ' - checker_id: 2':
            set_2.add(number_list[1])
        elif checker_id == ' - checker_id: 3':
            set_3.add(number_list[1])
        elif checker_id == ' - checker_id: 4':
            set_4.add(number_list[1])
        elif checker_id == ' - checker_id: 5':
            set_5.add(number_list[1])
        elif checker_id == ' - checker_id: 6':
            set_6.add(number_list[1])
        elif checker_id == ' - checker_id: 7':
            set_7.add(number_list[1])

print('1: ', len(set_1))
print('2: ', len(set_2))
print('3: ', len(set_3))
print('4: ', len(set_4))
print('5: ', len(set_5))
print('6: ', len(set_6))
print('7: ', len(set_7))


