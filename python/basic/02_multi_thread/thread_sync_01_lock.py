# 1. 用Lock来解决线程之间的同步问题

# RLock 可重入锁, 一个线程的内部, 可以多次acquire, 但是acquire和release的次数必须一致.
from threading import RLock

from threading import Lock
from threading import Thread

total = 0
# generate a lock
lock = Lock()

# generate a rlock
rlock = RLock()

def add():
    global total
    for i in range(100000):
        # get lock
        lock.acquire()
        total += 1
        # release lock
        lock.release()

        # get rlock the first time
        rlock.acquire()
        # get rlock the second time
        rlock.acquire()
        print("do something..")
        # release rlock the first time
        rlock.release()
        # release rlock the second time
        rlock.release()

def desc():
    global total
    for i in range(100000):
        # get lock
        lock.acquire()
        total -= 1
        # release lock
        lock.release()

if __name__ == '__main__':
    thread1 = Thread(target=add, daemon=True)
    thread2 = Thread(target=desc, daemon=True)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print(total)
