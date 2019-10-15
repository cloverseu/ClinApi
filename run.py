#object:
# 1.contain application
# 2.define flaskr as a package
# 项目的配置
# https://github.com/cloverseu/python-api-tesing/tree/master/flask/api_demo
from flask import Flask
from app import api_bp
from model.db import db
from flask_cors import CORS
from flask_mail import Mail


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    CORS(app)
    '''
    用于下载文件
    '''
    @app.route("/download/<filepath>", methods=['GET'])
    def download_file(filepath):
        # 此处的filepath是文件的路径，但是文件必须存储在static文件夹下， 比如images\test.
        return app.send_static_file(filepath)

    app.register_blueprint(api_bp, url_prefix='/api')
    db.init_app(app)
    return app


if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True)
    # app.config.update(
    #     DEBUG=True,
    #     MAIL_SERVER='smtp.live.com',
    #     MAIL_PROT=25,
    #     MAIL_USE_TLS=True,
    #     MAIL_USE_SSL=False,
    #     MAIL_USERNAME='example@hotmail.com',
    #     MAIL_PASSWORD='**********',
    #     MAIL_DEBUG=True
    # )
    #
    # mail = Mail(app)
    # app.run(debug=True, host="0.0.0.0")
