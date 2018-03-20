# -*- coding: utf-8 -*-
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import config
import smtplib
import time


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((
        Header(name, 'utf-8').encode(),
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


def send_mail(user_name, to_addr, stock_name, stock_code, price, rate):
    if rate > 0:
        flag_a, flag_b = u'卖出', u'涨幅'
    else:
        flag_a, flag_b = u'买入', u'跌幅'
    datetime = time.strftime("%H:%M:%S", time.localtime())
    msg = MIMEText('时间：%s\n名称：%s\n代码：%s\n现价：%.2f\n振幅：%.2f%%' %
                   (datetime, stock_name.encode("utf-8"), stock_code, float(price), rate), 'plain', 'utf-8')
    msg['From'] = _format_addr(u'股票监视器 <%s>' % config.EMAIL_FROM_ADDR)
    msg['To'] = _format_addr(u'%s <%s>' % (user_name, to_addr))
    msg['Subject'] = Header(u'【%s提醒】: %s（%s）%s: %.2f%%' %
                            (flag_a, stock_name, stock_code, flag_b, rate), 'utf-8').encode()
    server = smtplib.SMTP(config.EMAIL_SMTP_SERVER, 25)
    # server.set_debuglevel(1)
    server.login(config.EMAIL_FROM_ADDR, config.EMAIL_PASSWORD)
    server.sendmail(config.EMAIL_FROM_ADDR, [to_addr], msg.as_string())
    server.quit()

if __name__ == '__main__':
    send_mail('benheart', 'geek.hu@qq.com', u'中国平安', 'sh601318', '73', 4.78)
