import base64

if __name__ == '__main__':
    code = '1318'
    code_encrypt = ''
    print(base64.b64decode(code.encode()))