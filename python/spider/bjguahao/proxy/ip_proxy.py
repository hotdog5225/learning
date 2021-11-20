import requests
from bs4 import BeautifulSoup as bs
import re


class IPProxy:
    def __init__(self):
        url_list = []
        url_base = 'http://www.kxdaili.com/dailiip/1/'
        for i in range(11)[1:]:
            url = url_base + '{}.html'.format(i)
            url_list.append(url)
        self.url_list = url_list

        headers = {
            "Host": "www.kxdaili.com",
            "Connection": "keep-alive",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Referer": "http://www.kxdaili.com/dailiip/1/1.html",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
            "Cookie": "ASPSESSIONIDASTAQCCT=NOLLHHBAOPMJJCJHBEHAAJHH; __51cke__=; __tins__17751595=%7B%22sid%22%3A%201637368960327%2C%20%22vd%22%3A%205%2C%20%22expires%22%3A%201637370909396%7D; __51laig__=5",
            "x-tt-env": "boe_dpa_i18n_creative_platform",
        }
        session = requests.Session()
        session.headers = headers
        self.session = session

    def get_free_ip_porxies(self):
        for url in self.url_list:
            resp = self.session.get(url)
            html = resp.content.decode('utf-8')
            with open('test.html', 'w') as f:
                f.write(html)
            self.store_ip_list(html)
            exit()

    def store_ip_list(self, html):
        soup = bs(html, 'lxml')
        tr_tags = soup.find_all('tr')
        for tr_tag in tr_tags:
            th_tag_list = tr_tag.contents
            for idx, tag in enumerate(th_tag_list):
                if tag.string.strip() == "":
                    th_tag_list.pop(idx)
            # 代理等级 高匿
            th_tag_level = th_tag_list[2]
            # 代理类型 http / https
            th_tag_type = th_tag_list[3]
            if (th_tag_level.string == '高匿' and re.search('HTTPS',th_tag_type.string)):
                print(th_tag_list[0].string.strip())


if __name__ == '__main__':
    ip = IPProxy()
    ip.get_free_ip_porxies()
