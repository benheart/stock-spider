# -*- coding: utf-8 -*-
import config
import MySQLdb


def get_stock_conditions():
    stock_conditions_dict = {}
    # 打开数据库连接
    db = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, config.DB_DATABASE)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 查询预警条件
    sql = """SELECT id, user_id, stock_code, lower_price, higher_price, increase_rate, 
                 decrease_rate, is_remind FROM user_stock_remind"""
    try:
        # 执行SQL语句
        cursor.execute(sql)
        result = cursor.fetchall()
        for condition in result:
            remind_id, user_id, stock_code, lower_price, higher_price, increase_rate, decrease_rate, is_remind = \
                condition[0], condition[1], condition[2], condition[3], \
                condition[4], condition[5], condition[6], condition[7]
            if stock_code[0:2] == '00' or stock_code[0:2] == '30':
                stock_code = 'sz' + stock_code
            elif stock_code[0:2] == '60':
                stock_code = 'sh' + stock_code
            if stock_code not in stock_conditions_dict:
                conditions = [condition]
                stock_conditions_dict[stock_code] = conditions
            else:
                conditions = stock_conditions_dict[stock_code]
                conditions.append(condition)
                stock_conditions_dict[stock_code] = conditions
    except:
        print "Error: unable to fetch stock conditions"
    # 关闭数据库连接
    db.close()
    return stock_conditions_dict


def update_remind_flag(remind_id, is_remind):
    # 打开数据库连接
    db = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, config.DB_DATABASE)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 查询预警条件
    sql = """UPDATE user_stock_remind SET is_remind = %s WHERE id = %s""" % (is_remind, remind_id)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
        print "Error: fail to update stock remind flag"
    # 关闭数据库连接
    db.close()


def update_remind_price(remind_id, current_price, lower_price, higher_price):
    # 打开数据库连接
    db = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, config.DB_DATABASE)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 查询预警条件
    sql = """UPDATE user_stock_remind SET current_price = %s, lower_price = %s, higher_price = %s 
             WHERE id = %s""" % (current_price, lower_price, higher_price, remind_id)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
        print "Error: fail to update stock remind flag"
    # 关闭数据库连接
    db.close()
