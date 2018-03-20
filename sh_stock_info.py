# -*- coding: utf-8 -*-
import codecs
import json
import requests
import MySQLdb
import time
import config


def main():
    # 打开数据库连接
    db = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, config.DB_PASSWORD, config.DB_DATABASE)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 从文件读取上交所 A股 列表
    file_reader = codecs.open('sh_stock_list.txt', 'rb', encoding='utf-8')
    basic_url = 'http://query.sse.com.cn/commonQuery.do?isPagination=false&sqlId=COMMON_SSE_ZQPZ_GP_GPLB_C&productid=%s'
    date_url = 'http://query.sse.com.cn/commonQuery.do?isPagination=false&sqlId=COMMON_SSE_ZQPZ_GP_GPLB_AGSSR_C&productid=%s'
    shares_url = 'http://query.sse.com.cn/security/stock/queryCompanyStockStruct.do?&isPagination=false&companyCode=%s'
    headers = {'Referer': 'http://query.sse.com.cn'}
    for line in file_reader:
        data = line.split(',')
        print 'Process %s(%s)' % (data[1], data[0])
        # 基本信息
        url = basic_url % data[0]
        page = requests.get(url, headers=headers)
        basic_json = json.loads(page.text)
        # 上市日期
        url = date_url % data[0]
        page = requests.get(url, headers=headers)
        date_json = json.loads(page.text)
        listing_date_a = '0000-00-00'
        if date_json and len(date_json['result']) > 0:
            listing_date_a = date_json['result'][0]['LISTINGDATEA']
        # 股本结构
        url = shares_url % data[0]
        page = requests.get(url, headers=headers)
        shares_json = json.loads(page.text)
        # SQL 插入语句
        try:
            sql = """INSERT INTO stock_info
                          (company_code, company_abbr, fullname, fullname_in_english, company_address, security_code_a,
                          security_abbr_a, area_name_desc, csrc_code_desc, www_address, registration_date_a, a_shares, total_shares)
                             VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, %s)""" % \
                  (basic_json['result'][0]['COMPANY_CODE'],
                   basic_json['result'][0]['COMPANY_ABBR'],
                   basic_json['result'][0]['FULLNAME'],
                   basic_json['result'][0]['FULL_NAME_IN_ENGLISH'],
                   basic_json['result'][0]['COMPANY_ADDRESS'],
                   basic_json['result'][0]['SECURITY_CODE_A'],
                   basic_json['result'][0]['SECURITY_ABBR_A'],
                   basic_json['result'][0]['AREA_NAME_DESC'],
                   basic_json['result'][0]['CSRC_CODE_DESC'],
                   basic_json['result'][0]['WWW_ADDRESS'],
                   listing_date_a,
                   int(float(shares_json['result']['AShares'].strip()) * 10000),
                   int(float(shares_json['result']['totalShares'].strip()) * 10000))
        except:
            print "%s(%s) construct sql error" % (data[1], data[0])
            continue
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            print "%s(%s) insert data error" % (data[1], data[0])
            db.rollback()
        time.sleep(3)
    # 关闭数据库连接
    db.close()


if __name__ == '__main__':
    main()
