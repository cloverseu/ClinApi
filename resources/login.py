from flask import request
from flask_restful import Resource, reqparse
from  model.userModel import User, UserSchema
from  model.db import db, session
import jwt
import time




class LoginResource(Resource):


    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.header = request.headers
        self.parser.add_argument('username', type=str)
        self.parser.add_argument('password', type=str)


        # 增加

    def post(self):
        # 看传递过来的是formdata数据还是json数据
        try:
            headers = jwt.decode(self.header["Authorization"], 'secret', algorithms=['HS256'])
            return {"statusCode": "0",
                    "error": {
                        "message": "当前用户已经登录",
                        "errorCode": "400"
                        }
                    }
        except:
            json_data = self.parser.parse_args()

            if not json_data:
                return {"statusCode": "0",
                        "error": {
                                "message": "内容为空",
                                "errorCode": "403"
                            }
                        }, 403
            # data, errors = UserSchema().load(json_data, session=session)
            # if errors:
            #     return errors, 422

            user = User.query.filter_by(username=json_data.get("username")).first()
            print(user,json_data)
            if not user:
                return {"statusCode": "0",
                        "error": {
                            "message": "用户不存在",
                            "errorCode": "403"
                            }
                        }, 403
            if (user.password!=json_data.get("password")):
                return {"statusCode": "0",
                        "error": {
                            "message": "密码或用户名错误",
                            "errorCode": "403"
                            }
                        }, 403

            #更新登录时间
            user.userLastLoginTime =  time.ctime(time.time())
            session.commit()
            #添加token(密码加密后返回?)
            #secret可以写入配置文件中, 'exp':int(time.time())+8000
            token = jwt.encode({'userID': user.userID}, 'secret', algorithm='HS256')
            return {
                 "statusCode": "1",
                 "userInfo": {'username':user.username, 'userRealName':user.userRealName},
                 "token": token.decode('utf-8')
            }

            # 更新