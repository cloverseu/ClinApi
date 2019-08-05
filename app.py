#路径资源列表
from flask import Flask, Blueprint
from flask_restful import Api
from resources.user import UserResource
from resources.file import File

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(File, '/File')
api.add_resource(UserResource, '/User')
