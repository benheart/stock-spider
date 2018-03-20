# -*- coding: utf-8 -*-
import codecs
import re
import requests


def main():
    fw = codecs.open('sh_stock_list.txt', 'wb', encoding='utf-8')
    url = 'http://www.sse.com.cn/js/common/ssesuggestdata.js'
    page = requests.get(url)
    regex = '_t\\.push\\({val:\\"(.+)\\",val2:\\"(.+)\\",val3:\\"(.+)\\"}\\);'
    data_match = re.findall(regex, page.text)
    if data_match:
        for data in data_match:
            # 过滤 B 股
            if int(data[0]) > 900000:
                continue
            fw.write(data[0]+','+data[1]+','+data[2]+'\n')
    fw.close()


if __name__ == '__main__':
    main()
