#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request, redirect, url_for, Flask
import jwt
from flask_mail import Message, Mail
from config import MAIL_PASSWORD, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MIME_TYPE
# from email.header import Header
from email.mime.text import MIMEText

def auth_token(func):
    def deco(*args, **kwargs):
        header = request.headers
        print(header)
        headers = jwt.decode(header["Authentication"], 'secret', algorithms=['HS256'])
        res = func(*args, **kwargs, headers=headers)
        return res
        # try:
        #     headers = jwt.decode(header["Authorization"], 'secret', algorithms=['HS256'])
        #     res = func(*args, **kwargs, headers=headers)
        #     return res
        # # 之后的有错误这边仍然会有报错
        # except:
        #     return {"statusCode": "0",
        #             "error": {
        #                 "message": "无权限访问，请登录",
        #                 "errorCode": "403"
        #                 }
        #             }, 403

    return deco

def sendMail(title, recipients,*args):
    app = Flask(__name__)
    app.config['MAIL_SERVER'] = MAIL_SERVER
    app.config['MAIL_PORT'] = MAIL_PORT
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD

    mail = Mail(app)
    mail.init_app(app)
    #要把自己再抄送一遍
    msg = Message(title, sender="interclin@163.com", recipients=[recipients, "interclin@163.com"], charset='utf-8')
    #用户信息
    #创建/修改新用户发确认邮件
    print(args)
    if len(args)>3:
        txt = "亲爱的" + args[0] + "，<br>您好，管理员为您分配了新的任务。任务信息如下：<br><br>项目:" \
               + args[1] + "<br>任务名称：" + args[2] + "<br>任务描述：" + args[3] + "<br>截止日期：" +    args[4] + "<br><br>请登录查看相关信息，有问题请与我们联系<br>http://47.100.168.127:8866/ctms<br>系统管理员"
    else:
        txt = "亲爱的"+args[0]+"，<br>您好，管理员为您创建了新的用户。用户信息如下：<br><br>用户名:"\
           +args[1]+"<br>密码："+args[2]+"<br><br>请测试您的登录信息，有问题请与我们联系<br>http://47.100.168.127:8866/ctms<br>系统管理员"

    file = "E:\ClinApi\static\8.docx"
    with app.open_resource(file) as fp:
        print(MIME_TYPE[file.split('.',1)[-1]])
        msg.attach("8.docx", MIME_TYPE[file.split('.',1)[-1]],fp.read())

    #附件地址
    print(txt)
    #修改smptlib中的ascii内容为utf-8
    msg.html = txt.encode('utf-8')
    mail.send(msg)
