'''
response.json()方法
'''

import requests
import json

url = 'https://api.github.com/user'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
}

# 这个 网址 返回的内容不是html 而是标准的json
response = requests.get(url, headers=headers)

# str
data = response.content.decode()
# str-- dict
data_dict = json.loads(data)

# json() 自动将json字符串 转换成Python dict list
data = response.json()

print(data['message'])
