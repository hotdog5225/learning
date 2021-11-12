import os

if __name__ == '__main__':
    # 组成调用js的命令
    # node命令：node -e
    cmd = 'node -e "require(\\"%s\\").init(%s,%s)"' % ('./crypt', 3, 5)
    cmd2 = 'node -e "require(\\"%s\\").my_encrypt(%s)"' % ('./crypt', "123456")

    pipeline = os.popen(cmd)
    pipeline = os.popen(cmd2)

    # 读取结果
    result = pipeline.read()

    print('结果是:', result)
