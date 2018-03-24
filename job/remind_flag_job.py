# -*- coding: utf-8 -*-
import time
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from dao import remind_dao


def main():
    stock_conditions_dict = remind_dao.get_stock_conditions()
    while True:
        # 9：20 -> 4800, 11:40 -> 13200, 12:50 -> 17400, 15:10 -> 25800
        real_time = time.time() % (3600 * 24)
        if 4800 <= real_time <= 13200 or 17400 <= real_time <= 25800:
            try:
                print time.strftime("%H:%M:%S", time.localtime()), "clear remind flag..."
                for stock_code in stock_conditions_dict.keys():
                    conditions = stock_conditions_dict[stock_code]
                    for condition in conditions:
                        remind_dao.update_remind_flag(condition[0], False)
            except Exception as e:
                print "Time: %s, Error: %s" % (time.strftime("%H:%M:%S", time.localtime()), e)
        if real_time > 25800:
            print 'Time is over 15:10'
            break
        time.sleep(60 * 10)


if __name__ == '__main__':
    main()
