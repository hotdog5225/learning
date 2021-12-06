'''
2. 实现方式2: 通过继承Thread类, 覆写run方法
'''
import threading
import time


# 继承threading.Thread类
class GetUrls(threading.Thread):
    # 给线程自定义名字
    def __init__(self, name):
        super().__init__(name=name)

    def run(self):
        print("get urls start")
        time.sleep(2)
        print("get urls end")


# 继承threading.Thread类
class GetDetail(threading.Thread):
    # 给线程自定义名字
    def __init__(self, name):
        super().__init__(name=name)

    def run(self):
        print("get detail start")
        time.sleep(2)
        print("get detail end")


if __name__ == '__main__':
    thread1 = GetUrls("get_url")
    thread2 = GetDetail("get_detail")

    start_time = time.time()

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("time cost: {}".format(time.time() - start_time))
