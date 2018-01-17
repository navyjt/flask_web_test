
from threading import Thread
from flask import current_app, render_template
import smtplib
from . import mail
from email.mime.text import MIMEText
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

#此函数用来封装正确的邮箱地址
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_async_email(app,smtpserver,fromaddress,toaddress,msg):
    with app.app_context():
        smtpserver.sendmail(fromaddress,toaddress,msg)
        smtpserver.quit()


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()

    print(app.config['MAIL_SERVER'],app.config['MAIL_PORT'])

    smtpserver = smtplib.SMTP_SSL(app.config['MAIL_SERVER'],app.config['MAIL_PORT'])
    # qq和163邮箱均不支持startssl（）函数
    smtpserver.ehlo()
    # smtpserver.startssl()
    smtpserver.ehlo()

    smtpserver.login(app.config['MAIL_USERNAME'],app.config['MAIL_PASSWORD'])

    toaddress=to
    fromaddress = app.config['FLASKY_MAIL_SENDER']
    subject = app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject
    header = 'To:'+ toaddress +'\n'
    header = header + 'From:' + fromaddress +'\n'
    header = header + 'Subject:' +subject + '\n'
  
    body = render_template(template + '.txt', **kwargs)
    msg = MIMEText(body, 'plain', 'utf-8')

    msg['From'] = _format_addr('Python用户 <%s>' % fromaddress)
    msg['To'] = _format_addr('管理员 <%s>' % toaddress)
    msg['Subject'] = Header(subject, 'utf-8').encode()

    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    print(msg)
    print('###################################')

    # 多线程调用
    thr = Thread(target=send_async_email, args=[app,smtpserver,fromaddress,toaddress,msg.as_string()])
    thr.start()
    return thr
