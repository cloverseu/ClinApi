from flask import request
from flask_restful import Resource, reqparse
from  model.studyModel import Study, StudySchema
from common.util import auth_token
from  model.db import db, session
import datetime



class StudyResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        # self.parser.add_argument('file', type=FileStorage, location="files")
        # self.parser.add_argument('user_id', type=int)
        # self.parser.add_argument('study_id', type=int)
        # self.parser.add_argument('sop_name', type=str)
        # self.parser.add_argument('sop_description', type=str)

    #查询
    @auth_token
    def get(self, headers):
        studyInfo = Study.query.all()
        result = StudySchema().dump(studyInfo, many=True).data
        return {'message':'success', 'data':result}

    #增加
    @auth_token
    def post(self, headers):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        print(json_data)
        #接收的日期格式为2014-08-11T05:26:03.869245
        data, errors = StudySchema().load(json_data, session=session)
        if errors:
            return errors,422
        name = Study.query.filter_by(name=json_data['name']).first()
        if name:
            return {'message': 'name already exists'}, 400

        #变量如果没有会怎样,需要指定阶段文件？

        study = Study(
            name = json_data['name'],
            status_id = json_data['status_id'],
            user_id = json_data['user_id'],
            description = json_data['description'],
            plan_start_date= json_data['plan_start_date'],
            plan_end_date = json_data['plan_end_date']
            # plan_start_date = datetime.datetime.strptime(json_data['plan_start_date'], "%Y-%m-%d %H:%M:%S"),
            # plan_end_date = datetime.datetime.strptime(json_data['plan_end_date'],"%Y-%m-%d %H:%M:%S")
        )
        session.add(study)
        session.commit()

        return {'message': 'success','filename': study.study_id}

    #更新
    def put(self):
        json_data = request.get_json(force=True)
        data_user_id = json_data['studyID']
        update_user = session.query(Study).filter_by(studyID=data_user_id)
        update_user.update(json_data)
        session.commit()

        return {'message': 'success'}
    #
    # #删除
    def delete(self):
        json_data = request.get_json(force=True)
        data_user_id = json_data['studyID']
        del_by_id = session.query(Study).filter_by(studyID=data_user_id)
        session.delete(del_by_id)
        session.commit()

        return { 'message':'success'}


