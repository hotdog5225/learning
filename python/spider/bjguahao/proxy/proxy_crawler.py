import sys

sys.path.append("../utils/")
from get_page import get_page

import logging
import re

from bs4 import BeautifulSoup as bs


class ProxyMetaClass(type):
    def __new__(cls, name, base, attrs):
        count = 0
        attrs["__CrawlFunc__"] = []
        for k, v in attrs.items():
            if 'crawl' in k:
                attrs["__CrawlFunc__"].append(k)
                count += 1
        attrs["__CrawlFuncCount__"] = count
        return type.__new__(cls, name, base, attrs)

'''
爬取proxy
'''
class Crawler(metaclass=ProxyMetaClass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            logging.info("成功获取到代理: %s", proxy)
            proxies.append(proxy)
        return proxies

    def crawl_kxdaili(self):
        url_base = 'http://www.kxdaili.com/dailiip/1/{}.html'
        urls = [url_base.format(page_no) for page_no in range(1, 11)]
        for url in urls:
            html = get_page(url)
            soup = bs(html, 'lxml')
            tr_tags = soup.find_all('tr')
            for tr_tag in tr_tags:
                th_tag_list = tr_tag.contents
                for idx, tag in enumerate(th_tag_list):
                    if tag.string.strip() == "":
                        th_tag_list.pop(idx)
                # ip
                th_tag_ip = th_tag_list[0]
                # port
                th_tag_port = th_tag_list[1]
                # 代理等级 高匿
                th_tag_level = th_tag_list[2]
                # 代理类型 http / https
                th_tag_type = th_tag_list[3]
                if (th_tag_level.string == '高匿' and re.search('HTTPS', th_tag_type.string)):
                    yield ':'.join([th_tag_ip.string.strip(), th_tag_port.string.strip()])

if __name__ == '__main__':
    crawler = Crawler()
    generater = crawler.crawl_kxdaili()
    for proxy in generater:
        print(proxy)