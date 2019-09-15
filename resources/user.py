from flask import request
from flask_restful import Resource, reqparse
from  model.userModel import User, UserSchema
from model.user_projectModel import userProject,userProjectSchema
from  model.db import db, session
from  common.queryByItem import QueryConductor
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
        # userInfo = User.query.all()
        # userResult = UserSchema().dump(userInfo, many=True).data
        # userProjectResult = userProject
        # return {'message':'success', 'data':result}
        data = self.parser.parse_args()
        userInfo = QueryConductor(data).queryProcess()
        if not userInfo:
            userInfo = User.query.all()
        result = UserSchema().dump(userInfo, many=True).data
        userID = None
        for i, k in enumerate(result):
            userID = k["userID"]

        print(userID)
        user_projectInfo = userProject.query.filter_by(userID=userID).all()
        result_user_project = userProjectSchema().dump(user_projectInfo, many=True).data
        print(result_user_project)
        return {"statusCode": "1", 'users': result, "project":result_user_project}

    #增加
    @auth_token
    def post(self, headers):
        print(headers['userID'])
        #需要判断该用户是否有增加新用户的权限
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        print(json_data)
        data, errors = UserSchema().load(json_data, session=session)
        if errors:
            return errors,422
        user = User.query.filter_by(username=json_data['username']).first()
        if user:
            return {'message': 'user already exists'}, 400

        #变量如果没有会怎样
        user = User(
            username = json_data['username'],
            userRealName = json_data['userRealName'],
            password = json_data['password'],
            userEmail = json_data['userEmail'],
            isAdmin = json_data['isAdmin'],
            userAccountStatus = json_data['userAccountStatus'],
            userLastLoginTime = None
            # userLastLoginTime = json_data['userLastLoginTime']
            # email = json_data['email'],
            # date_create = datetime.datetime.now(),
            # is_admin = json_data['is_admin'],
            # can_createTrail = json_data['can_createTrail'],
            # can_createSop = json_data['can_createSop'],
            # is_active= json_data['is_active']
        )
        session.add(user)
        session.commit()

        return {"statusCode": "1"}

    #更新
    @auth_token
    def put(self, headers):
        json_data = request.get_json(force=True)
        data_user_id = json_data['userID']
        update_user = session.query(User).filter_by(userID=data_user_id)
        update_user.update(json_data)
        #更新方法，变量json_data中的所有数据
        # for k in json_data:
        #     update_user.update({k:json_data[k]})

        session.commit()
        return {"statusCode": "1"}

    #删除
    @auth_token
    def delete(self, headers):
        data = self.parser.parse_args()
        data_user_id = data.get('userID')
        del_by_id = session.query(User).filter_by(userID = data_user_id).first()
        session.delete(del_by_id)
        session.commit()

        return { "statusCode": "1"}