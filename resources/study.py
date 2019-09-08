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
    # def put(self):
    #     data = self.parser.parse_args()
    #     data_user_id = data.get('user_id')
    #     update_user = session.query(User).filter_by(user_id=data_user_id).first()
    #     update_user.password =  data.get('password')
    #     session.commit()
    #
    #     return {'message': 'success'}
    #
    # #删除
    # def delete(self):
    #     data = self.parser.parse_args()
    #     data_user_id = data.get('user_id')
    #     del_by_id = session.query(User).filter_by(user_id = data_user_id).first()
    #     session.delete(del_by_id)
    #     session.commit()
    #
    #     return { 'message':'success'}


