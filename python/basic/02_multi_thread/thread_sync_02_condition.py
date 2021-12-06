from threading import Thread
# 条件变量
from threading import Condition

class TiamMaoJingLing(Thread):
    def __init__(self, cond):
        super().__init__(name="天猫精灵")
        self.cond = cond

    def run(self):
        # 下面这句话是执行wait/notify的前提.
        # with就是调用了__enter__方法, 结束后执行__exit__方法
        with self.cond:
            print("小爱同学")
            # 唤醒最近等待的一个wait()线程
            self.cond.notify()
            # 阻塞, 等待notify将其唤醒
            self.cond.wait()

            print("我们来对古诗吧?")
            self.cond.notify()
            self.cond.wait()

class XiaoAiTongXue(Thread):
    def __init__(self, cond):
        super().__init__(name="小爱同学")
        self.cond = cond

    def run(self):
        with self.cond:
            self.cond.wait()
            print("在")
            self.cond.notify()


            self.cond.wait()
            print("好呀")
            self.cond.notify()

if __name__ == '__main__':
    cond = Condition()

    tianmao_thread = TiamMaoJingLing(cond)
    xiaoai_thread = XiaoAiTongXue(cond)

    # 启动顺序很重要
    # 首先要启动xiaoai_thread, 因为xiaoai_thread先启动self.cond.wait()方法. 用于接收notify信号
    xiaoai_thread.start()
    tianmao_thread.start()
