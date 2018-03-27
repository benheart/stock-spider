# -*- coding: utf-8 -*-
import re
import requests
import time
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import config
from util import email_sender
from dao import user_dao, remind_dao


def main():
    user_info_dict = user_dao.get_user_info()
    while True:
        # 9：25 -> 5100, 11:35 -> 12900, 12:55 -> 17700, 15:05 -> 25500
        real_time = time.time() % (3600 * 24)
        if 5100 <= real_time <= 12900 or 17700 <= real_time <= 25500:
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
                        rate = (float(data_str[3]) - float(data_str[2])) / float(data_str[2]) * 100
                        for condition in conditions:
                            if condition[7] == 1:
                                continue
                            user_info = user_info_dict[condition[1]]
                            if rate >= condition[5] or rate <= condition[6] \
                                    or float(data_str[3]) >= condition[4] or float(data_str[3]) <= condition[3]:
                                print "Time: %s, send email to %s start, stock: %s, price: %s" % \
                                      (time.strftime("%H:%M:%S", time.localtime()), user_info[2], data_str[0], data_str[3])
                                email_sender.send_mail(user_info[1], user_info[2], data_str[0], stock_code, data_str[3], rate)
                                remind_dao.update_remind_flag(condition[0], True)
                                print "Time: %s, send email successfully" % time.strftime("%H:%M:%S", time.localtime())
            except Exception as e:
                print "Time: %s, Error: %s" % (time.strftime("%H:%M:%S", time.localtime()), e)
        if real_time > 25500:
            print 'Time is over 15:05'
            break
        time.sleep(60)


if __name__ == '__main__':
    main()
