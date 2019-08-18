from flask import request
from flask_restful import Resource, reqparse
from  model.sopModel import sopFile, sopFileSchema
from  model.db import db, session
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import datetime
import os


class sopFileResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('file', type=FileStorage, location="files")
        self.parser.add_argument('user_id', type=int)
        self.parser.add_argument('study_id', type=int)
        self.parser.add_argument('sop_name', type=str)
        self.parser.add_argument('sop_description', type=str)


    #查询
    def get(self):
        sopInfo = sopFile.query.all()
        result = sopFileSchema().dump(sopInfo, many=True).data
        return {'message':'success', 'data':result}

    #增加
    def post(self):
        data = self.parser.parse_args()
        print(data)
        # json_data = request.get_json(force=True)
        # if not json_data:
        #     return {'message': 'No input data provided'}, 400
        # data, errors = sopFileSchema().load(json_data)
        # if errors:
        #     return errors,422
        # sop_name = sopFile.query.filter_by(sop_name=json_data['sop_name']).first()
        # if sop_name:
        #     return {'message': 'user already exists'}, 400

        #变量如果没有会怎样,需要指定阶段文件？
        file = data.get('file')
        if not file:
            return {'message': 'No input g file provided'}, 400
        try:
            filename = secure_filename(file.filename)
            file.save(os.path.join('./files/', filename))
        except:
            return {'message': 'file save error'}, 400

        sop = sopFile(
            sop_name = data.get('sop_name'),
            study_id = data.get('study_id'),
            user_id = data.get('user_id'),
            sop_date_create = datetime.datetime.now(),
            sop_description = data.get('sop_description')
        )
        session.add(sop)
        session.commit()

        return {'message':'success','filename':file.name}

    #更新
    def put(self):
        data = self.parser.parse_args()
        data_user_id = data.get('user_id')
        update_user = session.query(User).filter_by(user_id=data_user_id).first()
        update_user.password =  data.get('password')
        session.commit()

        return {'message': 'success'}

    #删除
    def delete(self):
        data = self.parser.parse_args()
        data_user_id = data.get('user_id')
        del_by_id = session.query(User).filter_by(user_id = data_user_id).first()
        session.delete(del_by_id)
        session.commit()

        return { 'message':'success'}


