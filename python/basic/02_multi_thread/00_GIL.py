# GIL: global Interpreter Lock
# GIL 保证在同一时刻, 只有一个线程在cpu上执行字节码, 也无法将多个线程映射到多个核上(无法发挥多核的优势)

# 使用dis package查看程序的字节码
# import dis
# def add(a):
#     a = a+1
#     return a
# print(dis.dis(add))
# """
#  7           0 LOAD_FAST                0 (a)
#               2 LOAD_CONST               1 (1)
#               4 BINARY_ADD
#               6 STORE_FAST               0 (a)
#
#   8           8 LOAD_FAST                0 (a)
#              10 RETURN_VALUE
# """

# 即使有了GIL, 也不能保证线程安全, 因为GIL在某些时刻会释放掉
# - 再执行一些字节码一些行数后, 会释放.
# - 根据时间片释放.
# - IO操作时候, 也会释放GIL.
total = 0
def add():
    global total
    for i in range(1000000):
        total += 1

def desc():
    global total
    for i in range(1000000):
        total -= 1

import threading
thread1 = threading.Thread(target=add)
thread2 = threading.Thread(target=desc)
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print(total) # 每次结果都不同

