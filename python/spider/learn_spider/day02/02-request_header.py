import urllib.request


def load_baidu():
    url = "https://www.baidu.com"
    header = {
        # 浏览器的版本
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "haha": "hehe"
    }

    #  添加request header
    # (1)方式1:创建请求对象时 (添加header)
    request = urllib.request.Request(url, headers=header)
    # (2)方式2: 动态的去添加head的信息
    request.add_header("User-Agent",
                       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")

    # 请求网络数据
    response = urllib.request.urlopen(request)
    print(response)

    data = response.read().decode("utf-8")

    # 获取到完整的url
    final_url = request.get_full_url()
    print(final_url)

    # 响应头
    # print(response.headers)

    # 获取request header
    # (1)(所有的header的信息)
    request_headers = request.headers
    print(request_headers)
    # (2)第二种方式打印指定的headers的信息
    request_headers = request.get_header("User-agent")  # 注意点:首字母需要大写,其他字母都小写
    print(request_headers)


load_baidu()
