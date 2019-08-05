#object:
# 1.contain application
# 2.define flaskr as a package
# 项目的配置
# https://github.com/cloverseu/python-api-tesing/tree/master/flask/api_demo
from flask import Flask
from app import api_bp
from model.db import db

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.register_blueprint(api_bp, url_prefix='/api')
    db.init_app(app)
    return app


if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True)
