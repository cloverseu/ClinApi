from flask import request
from flask_restful import Resource, reqparse
from  model.userModel import User, UserSchema
from  model.db import db, session
import datetime
from common.util import auth_token


class UserResource(Resource):


    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.header = request.headers
        self.parser.add_argument('userID', type=int)



    #查询
    @auth_token
    def get(self, headers):
        userInfo = User.query.all()
        result = UserSchema().dump(userInfo, many=True).data
        return {'message':'success', 'data':result}

    #增加
    @auth_token
    def post(self, headers):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        data, errors = UserSchema().load(json_data, session=session)
        if errors:
            return errors,422
        user = User.query.filter_by(username=json_data['username']).first()
        if user:
            return {'message': 'user already exists'}, 400

        #变量如果没有会怎样
        user = User(
            username = json_data['username']
            # password = json_data['password'],
            # email = json_data['email'],
            # date_create = datetime.datetime.now(),
            # is_admin = json_data['is_admin'],
            # can_createTrail = json_data['can_createTrail'],
            # can_createSop = json_data['can_createSop'],
            # is_active= json_data['is_active']
        )
        session.add(user)
        session.commit()

        return {'message':'success'}

    #更新
    @auth_token
    def put(self, headers):
        data = self.parser.parse_args()
        data_user_id = data.get('userID')
        update_user = session.query(User).filter_by(userID=data_user_id).first()
        # update_user.password =  data.get('password')
        session.commit()

        return {'message': 'success'}

    #删除
    @auth_token
    def delete(self, headers):
        data = self.parser.parse_args()
        data_user_id = data.get('userID')
        del_by_id = session.query(User).filter_by(userID = data_user_id).first()
        session.delete(del_by_id)
        session.commit()

        return { 'message':'success'}