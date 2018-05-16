#encoding = utf-8
from email.mime.text import MIMEText

msg = MIMEText("我在学python。", 'plain','utf-8')
msg['Subject'] = "测试"
msg['From'] = 'zj9005@163.com'
msg['To'] = '我的Outlook邮箱'

from_addr = 'zj9005@163.com'
password = input("password for 163mail: ")

to_addr = 'zj2011@live.com'
smtp_server = 'smtp.163.com'

import smtplib
server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
