import urllib.request
import urllib.parse
import string


def get_method_params():
    url = "http://www.baidu.com/s?wd="
    name = "美女"
    # 拼接字符串(汉字)
    final_url = url + name
    print(final_url)

    # 报错: UnicodeEncodeError: 'ascii' codec can't encode characters in position 10-11: ordinal not in range(128)
    # python:是解释性语言;解析器只支持 ascii 0 - 127, 不支持中文
    # 但是python可以接受转义后的数据, 如下
    # https://www.baidu.com/s?wd=%E7%BE%8E%E5%A5%B3
    # response = urllib.request.urlopen(final_url)

    # 代码发送了请求
    # url转译, string & urllib.parse
    # 将包含汉字的网址进行转译
    encode_new_url = urllib.parse.quote(final_url, safe=string.printable)
    print(encode_new_url)
    # 使用代码发送网络请求
    response = urllib.request.urlopen(encode_new_url)
    print(response)
    # 读取内容
    data = response.read().decode()
    print(data)
    # 保存到本地
    with open("02-encode.html", "w", encoding="utf-8") as f:
        f.write(data)

get_method_params()
