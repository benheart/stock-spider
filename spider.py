# -*- coding: utf-8 -*-
import re

import requests
from prettytable import PrettyTable


def main():
    table = PrettyTable(["股票名称", "涨跌幅", "当前价格", "今日最高价", "今日最低价", "今日开盘价", "昨日收盘价"])
    table.padding_width = 1  # 填充宽度
    url_base = 'http://hq.sinajs.cn/list=%s'
    stock_list = ['sh000001', 'sz000757', 'sh601318', 'sz000858', 'sh600036', 'sh601939', 'sz000001',
                  'sh600011', 'sh600050', 'sh600660', 'sh600623']
    for stock in stock_list:
        url = url_base % stock
        page = requests.get(url)
        regex = r'var hq_str_' + stock + '=\"(.+)\";'
        data_match = re.search(regex, page.text)
        if data_match:
            data = data_match.group(1)
            data_str = data.split(',')
            rate = (float(data_str[3]) - float(data_str[2])) / float(data_str[2]) * 100
            table.add_row([data_str[0], '%.2f%%' % rate, data_str[3], data_str[4], data_str[5], data_str[1], data_str[2]])
    print table

if __name__ == '__main__':
    main()
