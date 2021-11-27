import os

class Encryptor:
    def encrypt(self, ori_msg):
        # 组成调用js的命令
        # node命令：node -e
        cmd_encrypt = 'node -e "require(\\"%s\\").my_encrypt(%s)"' % ('./crypt/my_crypto', ori_msg)

        # 执行命令
        pipeline = os.popen(cmd_encrypt)

        # 读取结果
        encrypt_msg = pipeline.read()
        # print('加密后:', encrypt_msg)

        return encrypt_msg

if __name__ == '__main__':
    ori_msg = "16601126121"
    cmd_encrypt = 'node -e "require(\\"%s\\").my_encrypt(%s)"' % ('./my_crypto', ori_msg)

    # 执行命令
    pipeline = os.popen(cmd_encrypt)

    # 读取结果
    encrypt_msg = pipeline.read()
    print('加密后:', encrypt_msg)
