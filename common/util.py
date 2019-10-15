from flask import request, redirect, url_for, Flask
import jwt
from flask_mail import Message, Mail
from config import MAIL_PASSWORD, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME

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

def sendMail(title, recipients):
    app = Flask(__name__)
    app.config['MAIL_SERVER'] = MAIL_SERVER
    app.config['MAIL_PORT'] = MAIL_PORT
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD

    mail = Mail(app)
    mail.init_app(app)
    #要把自己再抄送一遍
    msg = Message(title, sender="interclin@163.com", recipients=[recipients, "interclin@163.com"])
    msg.html = "<b>testing1</b>"
    mail.send(msg)