import json
import logging

from fontTools.ttLib import TTFont

import os
from os import listdir
from os.path import isfile, join


class FontDecryptor:
    def __init__(self, redis):
        self.redis = redis

    def download_font(self, url):
        # 保存font文件
        f = os.popen("cd ./font_decrypt/font && curl -O https:{}".format(url))
        f.readlines()  # 阻塞
        return

    def get_code(self, url, str_code):
        # 判断font字体库是否存在, 不存在就下载
        font_name = url.strip().split('/')[-1]

        redis_key = "font_" + font_name
        if self.redis.exists(redis_key) == 0:
            logging.info(">>>>>>> download font: {}".format(font_name))
            self.download_font(url)
        else:
            return self.parse_font_string_from_redis(str_code, redis_key)

        # 新字体, 进行解析
        code = self.parse_font_string(font_name, str_code)

        # 拼接code, 返回
        return code

    def parse_font_string_from_redis(self, ori_str_code, font_redis_key):
        # base font mapping
        # font: eccbc87e4b5ce2fe28308fd9f2a7baf3
        # base_dict = {
        #     '0xf120': '0',
        #     '0xf29b': '1',
        #     '0xf032': '2',
        #     '0xf2d4': '3',
        #     '0xf23c': '4',
        #     '0xf315': '5',
        #     '0xf1f0': '6',
        #     '0xf38d': '7',
        #     '0xf201': '8',
        #     '0xf11d': '9',
        #     '0xf110': '.',
        # }

        font_map = json.loads(self.redis.get(font_redis_key))

        # 切分str_code
        str_code_list = [item.strip() for item in ori_str_code.strip().split(';')[:-1]]

        decrypt_str_code = ""
        for str_code in str_code_list:
            decrypt_str_code += font_map[int(str_code.replace(r'&#', '0'), 16)]

        return decrypt_str_code

    # get string && set font map to redis
    def parse_font_string(self, font_name, ori_str_code):
        # 切分str_code
        str_code_list = [item.strip() for item in ori_str_code.strip().split(';')[:-1]]
        # 格式化str_code
        str_code_list = [str_code.replace(r'&#x', '0x') for str_code in str_code_list]

        # base font
        font_base = TTFont('./font_decrypt/font/eccbc87e4b5ce2fe28308fd9f2a7baf3')
        # font_base.saveXML("eccbc87e4b5ce2fe28308fd9f2a7baf3.xml")

        if self.redis.get('font_eccbc87e4b5ce2fe28308fd9f2a7baf3') == 0:
            logging.error("can not get font base mapping in redis!")
            raise ValueError("can not get font base mapping in redis!")
        font_base_mapping_dict = {}
        try:
            font_base_mapping_dict = json.loads(self.redis.get('font_eccbc87e4b5ce2fe28308fd9f2a7baf3'))
        except Exception as e:
            print(e)

        # font to be parsed
        font_path_prefix = './font_decrypt/font/'
        font_parse = TTFont(join(font_path_prefix, font_name))
        # font_parse.saveXML(font_name + ".xml")

        # get cmap dict( unicode character -> glyf)
        cmap_base = self.get_proper_cmap(font_base)
        # {61490: '55954', 61712: '59406', 61725: '55903', 61728: '17526', 61936: '45488', 61953: '97108', 62012: '54221', 62107: '85956', 62164: '19425', 62229: '11262', 62349: '53982'}
        cmap_dict_base = cmap_base.cmap
        cmap_parse = self.get_proper_cmap(font_parse)
        cmap_dict_parse = cmap_parse.cmap

        # get glyf list
        # ['55954', '85956', '45488', '19425', '17526', '11262', '59406', '55903', '53982', '54221', '97108']
        font_base_order = font_base.getGlyphOrder()[1:]
        font_parse_order = font_parse.getGlyphOrder()[1:]

        # detail of base glyf
        f_base_flag = []
        for i in font_base_order:
            flags = font_base['glyf'][i].flags
            f_base_flag.append(list(flags))

        # detail of parse glyf
        f_parse_flag = []
        for i in font_parse_order:
            flags = font_parse['glyf'][i].flags
            f_parse_flag.append(list(flags))

        # 比对两个font
        font_parse_mapping_dict = {}
        for a, i in enumerate(f_base_flag):
            for b, j in enumerate(f_parse_flag):
                if self.cmp(i, j):
                    # 这两个index对应的glyf一样 , 生成映射表
                    base_key = self.get_glyf_key_in_hex_string(font_base_order[a], cmap_dict_base)
                    parse_key = self.get_glyf_key_in_hex_string(font_parse_order[b], cmap_dict_parse)
                    font_parse_mapping_dict[parse_key] = font_base_mapping_dict[base_key]

        self.redis.set('font_' + font_name, json.dumps(font_parse_mapping_dict))

        # get code string decrypted
        code = ""
        for item in str_code_list:
            code += font_parse_mapping_dict[item]
        return code

    def get_glyf_key_in_hex_string(self, glyf_decimal_str, cmap_dict):
        for key, glyf in cmap_dict.items():
            if glyf == glyf_decimal_str:
                return hex(key)

    def cmp(self, L1, L2):
        if len(L1) != len(L2):
            return 0
        for i in range(len(L2)):
            if L1[i] == L2[i]:
                pass
            else:
                return 0
        return 1

    def get_proper_cmap(self, font):
        for item in font['cmap'].tables:
            if not item.isUnicode():
                continue
            return item

        raise ValueError("no proper cmap (isUnicode)")


if __name__ == '__main__':
    fd = FontDecryptor()
    fd.download_font("//img.114yygh.com/fe/home/iconfont/c4ca4238a0b923820dcc509a6f75849b.html")
    pass

    # file_path = "./font"
    # onlyfiles = [f for f in listdir(file_path) if isfile(join(file_path, f))]
    # for file in onlyfiles:
    #     font = TTFont(join(file_path, file))
    #     font.saveXML(file + ".xml")
    #
    # font = TTFont("font/eccbc87e4b5ce2fe28308fd9f2a7baf3.ttf")
    # font.saveXML("ec.xml")
    #
    # font = TTFont("font/a87ff679a2f3e71d9181a67b7542122c")
    # font.saveXML('a8.xml')
