import urllib.request


def handler_openner():
    # 系统的urlopen并没有添加ip代理的功能所以需要我们自定义一个能够添加代理的handler
    # urlopen()的底层是通过opener.open()发起请求的, opener由handler构造而成.
    # urllib.request.urlopen()

    url = "https://blog.csdn.net/m0_37499059/article/details/79003731"

    # 创建自己的处理器handler
    handler = urllib.request.HTTPHandler()  # 最基础的handler, 无法添加ip代理
    # 创建自己的opener
    opener = urllib.request.build_opener(handler)

    # 用自己创建的opener调用open方法请求数据
    response = opener.open(url)
    # data = response.read()
    data = response.read().decode("utf-8")

    with open("02header.html", "w") as f:
        f.write(data)


handler_openner()
