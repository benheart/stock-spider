# -*- coding: utf-8 -*-
import config
import MySQLdb


def get_user_info():
    user_info_dict = {}
    # 打开数据库连接
    db = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, config.DB_DATABASE)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 查询用户信息
    sql = "SELECT user_id, name, email FROM user_info"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        result = cursor.fetchall()
        for user in result:
            user_id, name, email = user[0], user[1], user[2]
            user_info_dict[user_id] = user
    except:
        print "Error: unable to fetch users' info"
    # 关闭数据库连接
    db.close()
    return user_info_dict
