from flask import request
from flask_restful import Resource, reqparse
from  model.templateModel import Template, TemplateSchema
from  model.userModel import User, UserSchema
from  model.taskModel import Task
from  model.projectModel import Project
from  model.db import db, session
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from  common.queryByItem import QueryConductor
from common.util import auth_token
import datetime
import os
import re


class TemplateResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.header = request.headers
        self.parser.add_argument('templateName', type=str)
        self.parser.add_argument('templateID', type=int)
        # self.parser.add_argument('templateBelongedToTaskName', type=str)
        # self.parser.add_argument('templateBelongedToProjectName', type=str)
        # self.parser.add_argument('templateCreatorName', type=str)
        self.parser.add_argument('templateStatus', type=str)
        self.parser.add_argument('template', type=FileStorage, location="templates")
        # self.parser.add_argument('templateDescription', type=str)
        # self.parser.add_argument('templateBelongedToTaskID' , type=str)
        # self.parser.add_argument('templateBelongedToProjectID', type=str)
        # self.parser.add_argument('templateCreateDate', type=str)
        # self.parser.add_argument('templateCreatorID', type=str)
        # self.parser.add_argument('templateRemoveDate', type=str)
        # self.parser.add_argument('templateRemoveExecutorID', type=str)
        # self.parser.add_argument('templateDeleteDate', type=str)
        # self.parser.add_argument('templateDeleteExecutorID', type=str)
        # self.parser.add_argument('templateDownloadURL', type=str)

    #查询
    @auth_token
    def get(self, headers):
        data = self.parser.parse_args()
        taskTemplatesInfo = QueryConductor(data).queryProcess()
        if not taskTemplatesInfo:
            taskTemplatesInfo = Template.query.all()
        results = TemplateSchema().dump(taskTemplatesInfo , many=True).data
        for result in results:
            result["templateDownloadURL"] = "/download/"+result["templateDownloadURL"]
            result["templateCreatorName"] = session.query(User).filter_by(userID=result['templateCreatorID']).first().username
            result["templateRemoveExecutorName"] = session.query(User).filter_by(userID=result['templateRemoveExecutorID']).first().username
            result["templateDeleteExecutorName"] = session.query(User).filter_by(userID=result['templateDeleteExecutorID']).first().username
            # result["deleteExecutorName"] = session.query(User).filter_by(userID=result['deleteExecutorID']).first().username

        if (data.get("templateID")):
            return {"statusCode": "1", "template": results}
        else:
            return {"statusCode": "1", "templates": results}

        # return {"statusCode": "1", 'users': results}


    # 增加
    @auth_token
    def post(self, headers):
            data = self.parser.parse_args()
            print(data)
            # json_data = request.get_json(force=True)
            # if not json_data:
            #     return {'message': 'No input data provided'}, 400
            # data, errors = taskTemplatesSchema().load(json_data)
            # if errors:
            #     return errors,422
            # sop_name = taskTemplates.query.filter_by(sop_name=json_data['sop_name']).first()
            # if sop_name:
            #     return {'message': 'taskTemplate already exists'}, 400

            #变量如果没有会怎样,需要指定阶段文件？
            template = data.get('template')
            if not template:
                return {'message': 'No input  template provided'}, 400
            template_name = Template.query.filter_by(templateName=data.get('templateName')).first()



            taskTemplate = Template(
                templateName=data.get('templateName'),
                templateDescription = data.get('templateDescription'),
                templateCreateDate = data.get('templateCreateDate'),
                templateCreatorID = data.get('templateCreatorID'),
                templateStatus = data.get('templateStatus'),
                templateRemoveDate = data.get('templateRemoveDate'),
                templateRemoveExecutorID = data.get('templateRemoveExecutorID'),
                templateDeleteDate = data.get('templateDeleteDate'),
                templateDeleteExecutorID = data.get('templateDeleteExecutorID'),
                templateDownloadURL = data.get('templateDownloadURL')
            )

            if template_name:
                    return {'message': 'taskTemplate already exists'}, 400
            #略掉中文字符,文件不要有中文字符
            # templatename = secure_templatename(template.templatename)
            template.save(os.path.join('./static/', template.templateName))
            session.add(taskTemplate)
            session.commit()
                #return {'message': 'template save error'}, 400


            return {'message':'success','taskID':taskTemplate.templateID}


    # @auth_token
    # def post(self, headers):
    #     print(headers['userID'])
    #     # 需要判断该用户是否有增加新用户的权限
    #     json_data = request.get_json(force=True)
    #     if not json_data:
    #         return {'message': 'No input data provided'}, 400
    #     print(json_data)
    #     data, errors = TemplateSchema().load(json_data, session=session)
    #     if errors:
    #         return errors, 422
    #     template = Template.query.filter_by(templatename=json_data['templatename']).first()
    #     if template:
    #         return {'message': 'user already exists'}, 400
    #
    #     # 变量如果没有会怎样
    #     template_up = Template(
    #         templateName=json_data['templateName'],
    #         templateDescription = json_data['templateDescription'],
    #         templateBelongedToTaskID = json_data['templateBelongedToTaskID'],
    #         templateBelongedToProjectID = json_data['templateBelongedToProjectID'],
    #         templateCreateDate = json_data['templateCreateDate'],
    #         templateCreatorID = json_data['templateCreatorID'],
    #         templateStatus = json_data['templateStatus'],
    #         templateRemoveDate = json_data['templateRemoveDate'],
    #         templateRemoveExecutorID = json_data['templateRemoveExecutorID'],
    #         templateDeleteDate = json_data['templateDeleteDate'],
    #         templateDeleteExecutorID = json_data['templateDeleteExecutorID'],
    #         templateDownloadURL = json_data['templateDownloadURL']
    #     )
    #     session.add(template_up)
    #     session.commit()
    #
    #     return {"statusCode": "1"}

    # 更新
    @auth_token
    def put(self, headers):
        json_data = request.get_json(force=True)
        data_template_id = json_data['templateID']
        update_template = session.query(Template).filter_by(templateID=data_template_id)
        update_template.update(json_data)
        # 更新方法，变量json_data中的所有数据
        # for k in json_data:
        #     update_user.update({k:json_data[k]})
        session.commit()
        return {"statusCode": "1"}

    # 删除a
    @auth_token
    def delete(self, headers):
        data = self.parser.parse_args()
        data_template_id = data.get('templateID')
        del_by_id = session.query(User).filter_by(templateID=data_template_id).first()
        session.delete(del_by_id)
        session.commit()

        return {"statusCode": "1"}

