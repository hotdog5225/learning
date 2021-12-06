# 线程间通信
from queue import Queue
import time
import threading


def get_detail(url_queue):
    print(">>>>>>> get_detail")
    time.sleep(2)
    while not url_queue.empty():
        # get default is block
        url = url_queue.get()
        print(url)
        # indicate this enqueued item has been gotten, and all work on this item is DONE
        url_queue.task_done()


def get_urls(queue):
    print(">>>>>>> get_urls")
    for i in range(20):
        # default put is block
        queue.put("https://test.com/{id}".format(id=i))


if __name__ == '__main__':
    # 队列(线程安全)
    url_queue = Queue(maxsize=1000)

    # 起一个线程, 爬取url列表
    thread1 = threading.Thread(target=get_urls, daemon=True, args=(url_queue,)).start()

    # 起10个线程同时爬取详情页
    for i in range(10):
        get_detail_thread = threading.Thread(target=get_detail, daemon=True, args=(url_queue,)).start()

    start_time = time.time()

    # 主线程阻塞, 等待queue中的每个item都被gotten, 并且接收到了相应的task_done信号
    url_queue.join()

    print("time cost: {}".format(time.time() - start_time))
