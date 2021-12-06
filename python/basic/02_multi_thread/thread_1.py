'''
实现Thread的方式1: 通过Thread()实例化
'''

import time
import threading


def get_detail(url):
    print("get detail start")
    time.sleep(2)
    print("get detail end")


def get_urls(url):
    print("get urls start")
    time.sleep(2)
    print("get urls end")


if __name__ == '__main__':
    thread1 = threading.Thread(target=get_detail, args=("",))
    thread2 = threading.Thread(target=get_urls, args=("",))

    '''
    # Daemon守护线程, 当主线程退出时, 守护线程自动退出
    # thread1.setDaemon(True)
    # thread2.setDaemon(True)
    '''

    start_time = time.time()

    thread1.start()
    thread2.start()

    # 主线程阻塞, 等待子线程完成
    thread1.join()
    thread2.join()

    print("time cost: {}".format(time.time() - start_time))
