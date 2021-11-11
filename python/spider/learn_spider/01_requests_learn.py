import json

import requests

url = 'xxxxx'

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    'Cookie': 'xxxx',
}

cookie = {
    'cookie1': 'cookie1',
    'cookie2': 'cookie2',
}

# ===================================================================================================
'''
    send a request: get
'''

# no params set
response_get = requests.get(url, headers=header, cookies=cookie)

# send a request with multi params
# no need to urlencode or quote manually
params = {
    'wd': "美女",
    'wd2': "美女2"
}

free_proxy = {'http': '27.17.45.90:43411'}

response_get_multiparams = requests.get(url, headers=header, cookies=cookie, params=params, proxies=free_proxy)

# ignore SSL
# 因为https是有第三方CA证书认证的
# 但是 12306 虽然是https,但是它不是CA证书, 他是自己颁布的证书
# 解决方法 是: 告诉 web 我要忽略证书 访问(忽略风险) verify=False
response_no_ssl_verify = requests.get(url=url, headers=header, verify=False)

# ===================================================================================================
'''
    处理cookie
'''

# add cookie manually
#  cookies 的字符串
cookies = '_ga=GA1.2.1820447474.1535025127; MEIQIA_EXTRA_TRACK_ID=199Tty9OyANCXtHaSobJs67FU7J; WAF_SESSION_ID=7d88ae0fc48bffa022729657cf09807d; PHPSESSID=70kadg2ahpv7uuc8docd09iat4; _gid=GA1.2.133568065.1540383729; _gat=1; MEIQIA_VISIT_ID=1C1OdtdqpgpGeJ5A2lCKLMGiR4b; yaozh_logintime=1540383753; yaozh_user=381740%09xiaomaoera12; yaozh_userId=381740; db_w_auth=368675%09xiaomaoera12; UtzD_f52b_saltkey=ylH82082; UtzD_f52b_lastvisit=1540380154; UtzD_f52b_lastact=1540383754%09uc.php%09; UtzD_f52b_auth=f958AVKmmdzQ2CWwmr6GMrIS5oKlW%2BkP5dWz3SNLzr%2F1b6tOE6vzf7ssgZDjhuXa2JsO%2FIWtqd%2FZFelWpPHThohKQho; yaozh_uidhas=1; yaozh_mylogin=1540383756; MEIQIA_EXTRA_TRACK_ID=199Tty9OyANCXtHaSobJs67FU7J; WAF_SESSION_ID=7d88ae0fc48bffa022729657cf09807d; Hm_lvt_65968db3ac154c3089d7f9a4cbb98c94=1535025126%2C1535283389%2C1535283401%2C1539351081%2C1539512967%2C1540209934%2C1540383729; MEIQIA_VISIT_ID=1C1OdtdqpgpGeJ5A2lCKLMGiR4b; Hm_lpvt_65968db3ac154c3089d7f9a4cbb98c94=1540383761'
# 需要的是 dict
# (1) for循环创建dict
cook_dict = {}
cookies_list = cookies.split('; ')
for cookie in cookies_list:
    cook_dict[cookie.split('=')[0]] = cookie.split('=')[1]
# (2)字典推导式
cook_dict = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookies.split('; ')}

response = requests.get(url, headers=header, cookies=cook_dict)

# use session to auto save cookie
session = requests.session()
# 1.代码登录
login_url = 'https://www.yaozh.com/login'
login_form_data = {
    'username': 'xiaomaoera12',
    'pwd': 'lina081012',
    'formhash': '54AC1EE419',
    'backurl': 'https%3A%2F%2Fwww.yaozh.com%2F',
}
login_response = session.post(login_url, data=login_form_data, headers=header)
# 2.登录成功之后 带着 有效的cookies 访问 请求目标数据
data = session.get(url, headers=header).content.decode()

# ===================================================================================================
'''
    get response string & bytes
'''

# get bytes (preferred)
content = response_get.content
content_str = content.decode('utf-8')

# get json
content_json = json.loads(content_str)
# or
content_json = response_get.json()

# get string
text = response_get.text

# ===================================================================================================
'''
    get attrs
'''

# 1.获取请求头
request_headers = response_get.request.headers

# 2.获取响应头
coderesponse_headers = response_get.headers

# 3.响应状态码
code = response_get.status_code

# 4. 请求的cookie
request_cookie = response_get.request._cookies
print(request_cookie)

# 5. 响应的cookie
response_cookie = response_get.cookies
print(response_cookie)
