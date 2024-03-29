from flask import request
from flask_restful import Resource, reqparse
from  model.fileModel import File, FileSchema
from  model.userModel import User, UserSchema
from  model.taskModel import Task
from  model.projectModel import Project
from  model.db import db, session
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from  common.queryByItem import QueryConductor
from common.util import auth_token
import time
import os
import re
from sqlalchemy import or_


class FileResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.header = request.headers
        self.parser.add_argument('fileName', type=str)
        self.parser.add_argument('fileID')
        self.parser.add_argument('fileBelongedToTaskID', type=str)
        self.parser.add_argument('fileBelongedToProjectID', type=str)
        self.parser.add_argument('fileStatus', type=str)
        self.parser.add_argument('file', type=FileStorage, location="files")
        self.parser.add_argument('fileDescription', type=str)
        # self.parser.add_argument('fileBelongedToTaskID' , type=str)
        # self.parser.add_argument('fileBelongedToProjectID', type=str)
        # self.parser.add_argument('fileCreateDate', type=str)
        # self.parser.add_argument('fileCreatorID', type=str)
        # self.parser.add_argument('fileRemoveDate', type=str)
        # self.parser.add_argument('fileRemoveExecutorID', type=str)
        # self.parser.add_argument('fileDeleteDate', type=str)
        # self.parser.add_argument('fileDeleteExecutorID', type=str)
        # self.parser.add_argument('fileDownloadURL', type=str)

    #查询
    @auth_token
    def get(self, headers):
        data = self.parser.parse_args()
        if headers["isAdmin"]:
            cdt = {File.fileBelongedToTaskID > 0}
        else:
            taskExeCreateID =  Task.query.filter(*{or_(Task.taskCreatorID == headers["userID"], Task.taskExecutorID == headers["userID"])}).with_entities(Task.taskID).all()
            cdt = {File.fileBelongedToTaskID.in_(taskExeCreateID)}
        taskFilesInfo = QueryConductor(data, cdt).queryProcess()
        results = FileSchema().dump(taskFilesInfo, many=True)

        for result in results:
            result["fileDownloadURL"] = "/download/"+result["fileDownloadURL"]
            #result["fileCreatorName"] = session.query(User).filter_by(userID=result['fileCreatorID']).first().username
            #result["fileBelongedToTaskName"] = session.query(Task).filter_by(taskID=result['fileBelongedToTaskID']).first().taskName
            # result['fileBelongedToProjectID'] = session.query(Task).filter_by(taskID=result['fileBelongedToTaskID']).first().taskBelongedToProjectID
            # if result['fileBelongedToProjectID']:
            #     result["fileBelongedToProjectName"] = session.query(Project).filter_by(projectID=result['fileBelongedToProjectID']).first().projectName
            if result['fileRemoveExecutorID']:
                result["fileRemoveExecutorName"] = session.query(User).filter_by(userID=result['fileRemoveExecutorID']).first().username
            if result['fileDeleteExecutorID']:
                result["fileDeleteExecutorName"] = session.query(User).filter_by(userID=result['fileDeleteExecutorID']).first().username
            if result['fileDeleteExecutorID']:
                result["fileDeleteExecutorName"] = session.query(User).filter_by(userID=result['fileDeleteExecutorID']).first().username

        if (data.get("fileID")):
            return {"statusCode": "1", "file": results}
        else:
            return {"statusCode": "1", "files": results}

        # return {"statusCode": "1", 'users': results}


    # 增加
    @auth_token
    def post(self, headers):
            data = self.parser.parse_args()
            print(data)
            # json_data = request.get_json(force=True)
            # if not json_data:
            #     return {'message': 'No input data provided'}, 400
            # data, errors = taskFilesSchema().load(json_data)
            # if errors:
            #     return errors,422
            # sop_name = taskFiles.query.filter_by(sop_name=json_data['sop_name']).first()
            # if sop_name:
            #     return {'message': 'taskFile already exists'}, 400

            #变量如果没有会怎样,需要指定阶段文件？
            file = request.files['file']
            if not file:
                return {'message': 'No input  file provided'}, 400
            file_name = File.query.filter_by(fileName=data.get('fileName')).first()
            file_URL = File.query.filter_by(fileDownloadURL = file.filename).first()
            fileBelongedToTaskName = session.query(Task).filter_by(taskID=data.get('fileBelongedToTaskID')).first().taskName
            fileBelongedToProjectName = session.query(Project).filter_by(projectID=data.get('fileBelongedToProjectID')).first().projectName
            fileCreatorName = session.query(User).filter_by(userID=headers["userID"]).first().username

            taskFile = File(
                fileName = data.get('fileName'),
                fileDescription =  data.get('fileDescription'),
                fileBelongedToTaskID = data.get('fileBelongedToTaskID'),
                fileBelongedToProjectID = data.get('fileBelongedToProjectID'),
                fileCreateDate = time.ctime(time.time()),
                fileCreatorID = headers["userID"],
                fileStatus = data.get('fileStatus'),
                fileRemoveDate =  None,
                fileRemoveExecutorID =  None,
                fileDeleteDate =  None,
                fileDeleteExecutorID =  None,
                fileDownloadURL = file.filename,
                fileBelongedToTaskName = fileBelongedToTaskName,
                fileBelongedToProjectName = fileBelongedToProjectName,
                fileCreatorName = fileCreatorName
            # fileName = data.get('fileName'),
                # createDate = data.get('createDate'),
                # creatorID = data.get('creatorID'),
                # # self.creatorName = creatorName
                # description = data.get('description'),
                # deleteDate = data.get('deleteDate'),
                # deleteExecutorID = data.get('deleteExecutorID'),
                # # self.deleteExecutorName = deleteExecutorName
                # downloadURL = file.filename
            )

            if file_name:
                    return {'message': 'taskFile already exists'}, 400
            if file_URL:
                return {'message': 'File already exists, please rename'}, 400
            #略掉中文字符,文件不要有中文字符
            # filename = secure_filename(file.filename)
            file.save(os.path.join('./static/', file.filename))
            session.add(taskFile)
            session.commit()
                #return {'message': 'file save error'}, 400


            return {"statusCode": "1"}


    # @auth_token
    # def post(self, headers):
    #     print(headers['userID'])
    #     # 需要判断该用户是否有增加新用户的权限
    #     json_data = request.get_json(force=True)
    #     if not json_data:
    #         return {'message': 'No input data provided'}, 400
    #     print(json_data)
    #     data, errors = FileSchema().load(json_data, session=session)
    #     if errors:
    #         return errors, 422
    #     file = File.query.filter_by(filename=json_data['filename']).first()
    #     if file:
    #         return {'message': 'user already exists'}, 400
    #
    #     # 变量如果没有会怎样
    #     file_up = File(
    #         fileName=json_data['fileName'],
    #         fileDescription = json_data['fileDescription'],
    #         fileBelongedToTaskID = json_data['fileBelongedToTaskID'],
    #         fileBelongedToProjectID = json_data['fileBelongedToProjectID'],
    #         fileCreateDate = json_data['fileCreateDate'],
    #         fileCreatorID = json_data['fileCreatorID'],
    #         fileStatus = json_data['fileStatus'],
    #         fileRemoveDate = json_data['fileRemoveDate'],
    #         fileRemoveExecutorID = json_data['fileRemoveExecutorID'],
    #         fileDeleteDate = json_data['fileDeleteDate'],
    #         fileDeleteExecutorID = json_data['fileDeleteExecutorID'],
    #         fileDownloadURL = json_data['fileDownloadURL']
    #     )
    #     session.add(file_up)
    #     session.commit()
    #
    #     return {"statusCode": "1"}

    # 更新
    @auth_token
    def put(self, headers):
        # json_data = request.get_json(force=True)
        data = self.parser.parse_args()
        data_file_id = data.get("fileID")
        # data_file_id = json_data['fileID']
        update_file = session.query(File).filter_by(fileID=data_file_id).first()
        if data.get('fileName'):
            update_file.fileName = data.get('fileName')
        if data.get('fileDescription'):
            update_file.fileDescription = data.get('fileDescription')
        if  data.get('fileStatus'):
            update_file.fileStatus = data.get('fileStatus')

        if data.get('fileStatus') == "2":
            update_file.fileRemoveID  = headers["userID"]
            update_file.fileRemoveDate = time.ctime(time.time())

        # update_file.update()
        # 更新方法，变量json_data中的所有数据
        # for k in json_data:
        #     update_user.update({k:json_data[k]})
        session.commit()
        return {"statusCode": "1"}

    # 删除a
    @auth_token
    def delete(self, headers):
        data = self.parser.parse_args()
        data_file_id = data.get('fileID')
        del_by_id = session.query(File).filter_by(fileID=data_file_id).first()
        session.delete(del_by_id)
        session.commit()

        return {"statusCode": "1"}

    # def __init__(self):
    #     self.parser = reqparse.RequestParser()
    #     # self.parser.add_argument('file', type=FileStorage, location="files")
    #     self.parser.add_argument('belongedToTaskID', type=int)
    #     self.parser.add_argument('fileName', type=str)
    #     self.parser.add_argument('fileID', type=int)
    #     self.parser.add_argument('createDate', type=str)
    #     self.parser.add_argument('creatorID', type=int)
    #     self.parser.add_argument('description', type=str)
    #     self.parser.add_argument('deleteDate', type=str)
    #     self.parser.add_argument('deleteExecutorID', type=int)
    #     self.parser.add_argument('file', type=FileStorage, location="files")
    #
    #
    #
    # #查询
    # @auth_token
    # def get(self, headers):
    #     data = self.parser.parse_args()
    #     # data_trial_id = data.get('fileID')
    #     # data_user_id = data.get('creatorID')
    #     # print(data_user_id)
    #     # if (data_trial_id or data_user_id):
    #     #     taskFilesInfo = taskFiles.query.filter_by(creatorID=data_user_id)
    #     #     print(taskFilesInfo)
    #     # else:
    #     #     taskFilesInfo = taskFiles.query.all()
    #     # taskFilesInfo = taskFiles.query.all()
    #     taskFilesInfo = QueryConductor(data).queryProcess()
    #     if not taskFilesInfo:
    #         taskFilesInfo = taskFiles.query.all()
    #     result = taskFileSchema().dump(taskFilesInfo , many=True).data
    #     for r in result:
    #         print(r["fileID"])
    #         r["downloadURL"] = "/download/"+r["downloadURL"]
    #         r["creatorName"] = session.query(User).filter_by(userID=r['creatorID']).first().userName
    #         r["deleteExecutorName"] = session.query(User).filter_by(userID=r['deleteExecutorID']).first().userName
    #     return {'message':'success', 'taskFilesInfo':result}
    #
    # #增加
    # @auth_token
    # def post(self, headers):
    #     data = self.parser.parse_args()
    #     print(data)
    #     # json_data = request.get_json(force=True)
    #     # if not json_data:
    #     #     return {'message': 'No input data provided'}, 400
    #     # data, errors = taskFilesSchema().load(json_data)
    #     # if errors:
    #     #     return errors,422
    #     # sop_name = taskFiles.query.filter_by(sop_name=json_data['sop_name']).first()
    #     # if sop_name:
    #     #     return {'message': 'taskFile already exists'}, 400
    #
    #     #变量如果没有会怎样,需要指定阶段文件？
    #     file = data.get('file')
    #     if not file:
    #         return {'message': 'No input  file provided'}, 400
    #     file_name = taskFiles.query.filter_by(fileName=data.get('fileName')).first()
    #
    #
    #
    #     taskFile = taskFiles(
    #         belongedToTaskID = data.get('belongedToTaskID'),
    #         fileName = data.get('fileName'),
    #         createDate = data.get('createDate'),
    #         creatorID = data.get('creatorID'),
    #         # self.creatorName = creatorName
    #         description = data.get('description'),
    #         deleteDate = data.get('deleteDate'),
    #         deleteExecutorID = data.get('deleteExecutorID'),
    #         # self.deleteExecutorName = deleteExecutorName
    #         downloadURL = file.filename
    #     )
    #
    #     if file_name:
    #             return {'message': 'taskFile already exists'}, 400
    #     #略掉中文字符,文件不要有中文字符
    #     # filename = secure_filename(file.filename)
    #     file.save(os.path.join('./static/', file.filename))
    #     session.add(taskFile)
    #     session.commit()
    #         #return {'message': 'file save error'}, 400
    #
    #
    #     return {'message':'success','taskID':taskFile.fileID}
    #
    # #更新
    # @auth_token
    # def put(self, headers):
    #     data = self.parser.parse_args()
    #     data_taskFile_id = data.get('taskFile_id')
    #     update_taskFile = session.query(taskFiles).filter_by(fileID=data_taskFile_id).first()
    #     #update_taskFile.password =  data.get('password')
    #     session.commit()
    #
    #     return {'message': 'success'}
    #
    # #删除
    # @auth_token
    # def delete(self, headers):
    #     data = self.parser.parse_args()
    #     data_taskFile_id = data.get('fileID')
    #     del_by_id = session.query(taskFiles).filter_by(fileID = data_taskFile_id).first()
    #     session.delete(del_by_id)
    #     session.commit()
    #
    #     return { 'message':'success'}


