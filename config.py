# -*- coding: utf-8 -*-

# 发邮件配置
EMAIL_FROM_ADDR = 'username@163.com'
EMAIL_PASSWORD = 'token'
EMAIL_SMTP_SERVER = 'smtp.163.com'

# 数据库配置
DB_HOST = 'host'
DB_USERNAME = 'username'
DB_PASSWORD = 'password'
DB_DATABASE = 'database'

# 股票爬虫配置
real_time_url = 'http://hq.sinajs.cn/list=%s'
real_time_regex = r'var hq_str_%s=\"(.+)\";'
