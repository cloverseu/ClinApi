#路径资源列表
from flask import Flask, Blueprint
from flask_restful import Api
from resources.user import UserResource
from resources.sop import sopFileResource
from resources.study import StudyResource
from resources.project import   ProjectResource
from resources.tasks import TasksResource
from resources.taskFiles import taskFilesResource
from resources.login import LoginResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(sopFileResource, '/sopFile')
api.add_resource(StudyResource, '/Study')
api.add_resource(UserResource, '/User')
api.add_resource(ProjectResource, '/projectInfo')
api.add_resource(TasksResource, '/tasksInfo')
api.add_resource(taskFilesResource, '/taskFiles')
api.add_resource(LoginResource, '/login')


