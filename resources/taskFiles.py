from flask import request
from flask_restful import Resource, reqparse
from  model.taskFilesModel import taskFiles, taskFileSchema
from  model.userModel import User, UserSchema
from  model.db import db, session
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from  common.queryByItem import QueryConductor
from common.util import auth_token
import datetime
import os
import re


class taskFilesResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        # self.parser.add_argument('file', type=FileStorage, location="files")
        self.parser.add_argument('belongedToTaskID', type=int)
        self.parser.add_argument('fileName', type=str)
        self.parser.add_argument('fileID', type=int)
        self.parser.add_argument('createDate', type=str)
        self.parser.add_argument('creatorID', type=int)
        self.parser.add_argument('description', type=str)
        self.parser.add_argument('deleteDate', type=str)
        self.parser.add_argument('deleteExecutorID', type=int)
        self.parser.add_argument('file', type=FileStorage, location="files")



    #查询
    @auth_token
    def get(self, headers):
        data = self.parser.parse_args()
        # data_trial_id = data.get('fileID')
        # data_user_id = data.get('creatorID')
        # print(data_user_id)
        # if (data_trial_id or data_user_id):
        #     taskFilesInfo = taskFiles.query.filter_by(creatorID=data_user_id)
        #     print(taskFilesInfo)
        # else:
        #     taskFilesInfo = taskFiles.query.all()
        # taskFilesInfo = taskFiles.query.all()
        taskFilesInfo = QueryConductor(data).queryProcess()
        if not taskFilesInfo:
            taskFilesInfo = taskFiles.query.all()
        result = taskFileSchema().dump(taskFilesInfo , many=True).data
        for r in result:
            print(r["fileID"])
            r["downloadURL"] = "/download/"+r["downloadURL"]
            r["creatorName"] = session.query(User).filter_by(userID=r['creatorID']).first().userName
            r["deleteExecutorName"] = session.query(User).filter_by(userID=r['deleteExecutorID']).first().userName
        return {'message':'success', 'taskFilesInfo':result}

    #增加
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
        file = data.get('file')
        if not file:
            return {'message': 'No input  file provided'}, 400
        file_name = taskFiles.query.filter_by(fileName=data.get('fileName')).first()



        taskFile = taskFiles(
            belongedToTaskID = data.get('belongedToTaskID'),
            fileName = data.get('fileName'),
            createDate = data.get('createDate'),
            creatorID = data.get('creatorID'),
            # self.creatorName = creatorName
            description = data.get('description'),
            deleteDate = data.get('deleteDate'),
            deleteExecutorID = data.get('deleteExecutorID'),
            # self.deleteExecutorName = deleteExecutorName
            downloadURL = file.filename
        )

        if file_name:
                return {'message': 'taskFile already exists'}, 400
        #略掉中文字符,文件不要有中文字符
        # filename = secure_filename(file.filename)
        file.save(os.path.join('./static/', file.filename))
        session.add(taskFile)
        session.commit()
            #return {'message': 'file save error'}, 400


        return {'message':'success','taskID':taskFile.fileID}

    #更新
    @auth_token
    def put(self, headers):
        data = self.parser.parse_args()
        data_taskFile_id = data.get('taskFile_id')
        update_taskFile = session.query(taskFiles).filter_by(fileID=data_taskFile_id).first()
        #update_taskFile.password =  data.get('password')
        session.commit()

        return {'message': 'success'}

    #删除
    @auth_token
    def delete(self, headers):
        data = self.parser.parse_args()
        data_taskFile_id = data.get('fileID')
        del_by_id = session.query(taskFiles).filter_by(fileID = data_taskFile_id).first()
        session.delete(del_by_id)
        session.commit()

        return { 'message':'success'}


