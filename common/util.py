from flask import request, redirect, url_for
import jwt

def auth_token(func):
    def deco(*args, **kwargs):
        header = request.headers
        print(header)
        try:
            headers = jwt.decode(header["Authorization"], 'secret', algorithms=['HS256'])
            res = func(*args, **kwargs, headers=headers)
            return res
        # 之后的有错误这边仍然会有报错
        except:
            return {"statusCode": "0",
                    "error": {
                        "message": "无权限访问，请登录",
                        "errorCode": "403"
                        }
                    }, 403

    return deco
