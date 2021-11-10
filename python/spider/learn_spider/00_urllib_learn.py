import string
import urllib.request
import urllib.parse
import random
from http import cookiejar

'''
    get url only with ASCII
'''

url = 'https://www.baidu.com'  # url just with ASCII

# request: get
response = urllib.request.urlopen(url)  # OK, response:http响应的对象(响应体)

# =========================================================================================

'''
    get url with CN params, which is Unicode
'''

# url with CN params, need to be urlencoded
url_with_CN_params = url + '/s?wd=' + '美女'

# if direct get the url(with CN param, which is Unicode), Error will be raised:
# UnicodeEncodeError: 'ascii' codec can't encode characters in position 10-11: ordinal not in range(128)
response = urllib.request.urlopen(url_with_CN_params)

# python:是解释性语言;解析器只支持 ascii 0 - 127, 不支持中文
# 但是python可以接受转义后的数据, 如下
# https://www.baidu.com/s?wd=%E7%BE%8E%E5%A5%B3
url_quoted = urllib.parse.quote(url_with_CN_params, safe=string.printable)
response = urllib.request.urlopen(url_quoted)  # OK

# =========================================================================================

'''
    url with multi params
'''

params = {
    'param1': 1,
    'param2': 2,
    'param3': 3,
}
# url need to be encoded to "key=value"
param_encoded = urllib.parse.urlencode(params)
# if CN in contained, need to be quoted
param_quoted = urllib.parse.quote(param_encoded, safe=string.printable)

# =========================================================================================

'''
    读取响应体内容 <class 'bytes'>
'''

data = response.read()

# =========================================================================================

'''
    读取响应体内容 <class 'bytes'>
'''

# python爬取的类型:str bytes
# 如果爬取回来的是bytes类型:但是你写入的时候需要字符串 decode("utf-8")
# 如果爬取过来的是str类型:但你要写入的是bytes类型 encode(""utf-8")

# 将文件获取的内容转换成字符串 bytes -> string
str_data = data.decode('utr-8')

# 将数据写入文件 str写入文件
with open('baidu.html', 'w', encoding='utf-8') as f:
    f.write(data)
with open('baidu.html', 'w') as f:
    f.write(str_data)

# =========================================================================================

'''
    将字符串类型转换成bytes string -> bytes
'''
data = str_data.encode('utf-8')

# =========================================================================================

'''
    add header to a request body
'''

# because urlopen() method not supported for a Header added, we need to create a Request Body
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    # manually add a cookie
    'Cookie': 'xxxx',
}

# (1)方式1:创建请求对象时 (添加header)
request_object = urllib.request.Request(url, headers=header)
# (2)方式2: 动态的去添加head的信息
request_object.add_header("User-Agent",
                          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")

# instead of urlopen(url), now urlopen(request_object)
urllib.request.urlopen(request_object)

# =========================================================================================

'''
    get response header
'''
print(response.headers)

# =========================================================================================

'''
    get request header
'''

# (1)(所有的header的信息)
request_headers = request_object.headers
print(request_headers)
# (2)第二种方式打印指定的headers的信息
request_headers = request_object.get_header("User-agent")  # 注意点:首字母需要大写,其他字母都小写
print(request_headers)

# =========================================================================================

'''
    get a random user-agent: user-agent pool
'''

user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50"

]
# 每次请求的浏览器都是不一样的
random_user_agent = random.choice(user_agent_list)

# =========================================================================================

'''
    create a default handler: HTTPHandler
'''

# create a handler(many types, choose as your need)
handerl = urllib.request.HTTPHandler()
opener = urllib.request.build_opener(handerl)
# send request with opener
response_opener = opener.open(url)

print(response_opener.read().decode('utf-8'))

# =========================================================================================

'''
    # if you want to add a IP proxy, you need to create a handler of your own.
    # then generate a opener to send request.
'''

proxy_dict = {
    # 免费的写法
    # "http":"120.77.249.46:8080"
    # 付费的代理
    # "http":"xiaoming":123@115.
}
proxy_handler = urllib.request.ProxyHandler(proxies=proxy_dict)
proxy_opener = urllib.request.build_opener(proxy_handler)
# send request, we need to filter proxies that really work! (especially free proxies), so we add a timeout
try:
    response_proxy_opener = proxy_opener.open(url, timeout=1)
    data = response_proxy_opener.read().decode('utf-8')
except Exception as e:
    print(e)

# =========================================================================================

"""
    # use (CookieJar) to save Cookie

    获取 个人中心的页面

    1. 访问登录页, 登录成功后, cookie被set, 被CookieJar保存.
    2. 后续其他的api访问, 都会自动带着cookie
"""

# 1.1 登录的网址
login_url = 'https://www.yaozh.com/login'
# 1.2 登录的参数
login_form_data = {
    "username": "xiaomaoera12",
    "pwd": "lina081012",
    "formhash": "CE3ADF28C5",
    "backurl": "https%3A%2F%2Fwww.yaozh.com%2F"

}
# 1.3 登录
# build opener with cookie_handler
cookie_jar = cookiejar.CookieJar()
cookie_handler = urllib.request.HTTPCookieProcessor(cookie_jar)
cookie_opener = urllib.request.build_opener(cookie_handler)
# build request
form_data_encoded = urllib.parse.urlencode(login_form_data)  # urlencode
form_data_encoded_quoted = urllib.parse.quote(form_data_encoded).encode(encoding='utf-8')  # quoted, Unicode->ASCII
# post (has param data)
request_cookie = urllib.request.Request(login_url, data=form_data_encoded_quoted, headers=header)
# 如果登录成功, cookiejar会自动保存cookie
cookie_opener.open(request_cookie)

# 1.4 利用保存了cookie的opener, 去访问其他的网页
# build request
another_url = "www.xxx.com"
another_request = urllib.request.Request(another_url, headers=header)
response_cookie = cookie_opener.open(another_request)
print(response_cookie.read().decode('utf-8'))
