# -*- coding: utf-8 -*-
import re
import requests
import time
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import config
from dao import remind_dao


def main():
    try:
        stock_conditions_dict = remind_dao.get_stock_conditions()
        for stock_code in stock_conditions_dict.keys():
            conditions = stock_conditions_dict[stock_code]
            url = config.real_time_url % stock_code
            page = requests.get(url)
            regex = config.real_time_regex % stock_code
            data_match = re.search(regex, page.text)
            if data_match:
                data = data_match.group(1)
                data_str = data.split(',')
                stock_name, current_price = data_str[0].encode("utf-8"), float(data_str[3])
                for condition in conditions:
                    print "Time: %s, update remind info start, stock: %s, price: %.2f" % \
                          (time.strftime("%H:%M:%S", time.localtime()), stock_name, current_price)
                    lower_price, higher_price = current_price * (1 + condition[6]/100), current_price * (1 + condition[5]/100)
                    remind_dao.update_remind_price(condition[0], current_price, round(lower_price, 2), round(higher_price, 2))
                    print "Time: %s, update remind info successfully" % time.strftime("%H:%M:%S", time.localtime())

    except Exception as e:
        print "Time: %s, Error: %s" % (time.strftime("%H:%M:%S", time.localtime()), e)


if __name__ == '__main__':
    main()
