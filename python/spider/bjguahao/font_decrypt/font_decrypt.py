import logging

from fontTools.ttLib import TTFont

import os
from os import listdir
from os.path import isfile, join


class FontDecryptor:
    def download_font(self, url):
        # 保存font文件
        f = os.popen("cd ./font_decrypt/font && curl -O https:{}".format(url))
        f.readlines()  # 阻塞
        return

    def get_code(self, url, str_code):
        # 判断font字体库是否存在, 不存在就下载
        font_name = url.strip().split('/')[-1]
        font_path_prefix = './font_decrypt/font/'
        font_list = listdir(font_path_prefix)
        if font_name not in font_list:
            logging.info(">>>>>>> download font: {}".format(font_name))
            self.download_font(url)

        # 切分str_code
        str_code_list = str_code.strip().split(';')[:-1]
        # 格式化str_code
        str_code_list = [str_code.replace(r'&#x', '0x') for str_code in str_code_list]

        code_result = ""
        for str_code in str_code_list:
            # 识别code
            code = self.parse_font(font_name, str_code)
            code_result += code

        # 拼接code, 返回
        return code_result

    def parse_font(self, font_name, str_code):
        base_dict = {
            '0xf120': '0',
            '0xf29b': '1',
            '0xf032': '2',
            '0xf2d4': '3',
            '0xf23c': '4',
            '0xf315': '5',
            '0xf1f0': '6',
            '0xf38d': '7',
            '0xf201': '8',
            '0xf11d': '9',
            '0xf110': '.',
        }

        tmp_order = [2, 1, 6, 3, 0, 5, '.', 9, 7, 4, 8]

        # base font
        font_base = TTFont('./font_decrypt/font/eccbc87e4b5ce2fe28308fd9f2a7baf3')
        font_base.saveXML("eccbc87e4b5ce2fe28308fd9f2a7baf3.xml")

        # font to be parsed
        font_path_prefix = './font_decrypt/font/'
        font_parse = TTFont(join(font_path_prefix, font_name))
        font_parse.saveXML(font_name + ".xml")

        # get cmap dict( unicode character -> glyf)
        cmap_base = self.get_proper_cmap(font_base)
        cmap_dict_base = cmap_base.cmap
        cmap_parse = self.get_proper_cmap(font_parse)
        cmap_dict_parse = cmap_parse.cmap

        # get glyfOrder
        font_base_order = font_base.getGlyphOrder()[1:]
        font_parse_order = font_parse.getGlyphOrder()[1:]

        f_base_flag = []
        for i in font_base_order:
            flags = font_base['glyf'][i].flags
            f_base_flag.append(list(flags))

        f_parse_flag = []
        for i in font_parse_order:
            flags = font_parse['glyf'][i].flags
            f_parse_flag.append(list(flags))

        # 比对两个font
        result_dict = {}
        for a, i in enumerate(f_base_flag):
            for b, j in enumerate(f_parse_flag):
                if self.cmp(i, j):
                    key = font_parse_order[b].replace('uni', '')
                    key = eval(r'u"\u' + str(key) + '"').lower()
                    result_dict[key] = f_parse_flag[a]
        return result_dict

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
