import os

if __name__ == '__main__':
    # 组成调用js的命令
    # node命令：node -e
    cmd_encrypt = 'node -e "require(\\"%s\\").my_encrypt(%s)"' % ('./my_crypto', "16601126121")

    # 执行命令
    pipeline = os.popen(cmd_encrypt)

    # 读取结果
    result = pipeline.read()

    print('结果是:', result)
