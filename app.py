#路径资源列表
from flask import Flask, Blueprint
from flask_restful import Api
from resources.user import UserResource
from resources.sop import sopFileResource
from resources.study import StudyResource
from resources.project import   ProjectResource
from resources.task import TaskResource
from resources.file import FileResource
from resources.login import LoginResource
from resources.template import TemplateResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(sopFileResource, '/sopFile')
api.add_resource(StudyResource, '/study')
api.add_resource(UserResource, '/user')
api.add_resource(ProjectResource, '/project')
api.add_resource(TaskResource, '/task')
api.add_resource(FileResource, '/file')
api.add_resource(LoginResource, '/login')
api.add_resource(TemplateResource, '/template')


