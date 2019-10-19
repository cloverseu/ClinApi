from flask import request
from flask_restful import Resource, reqparse
from  model.userModel import User, UserSchema
from model.user_projectModel import userProject,userProjectSchema
from model.projectModel import Project,ProjectSchema
from  model.db import db, session
from  common.queryByItem import QueryConductor
import datetime
from common.util import auth_token
from common.util import sendMail
import json


class UserResource(Resource):


    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.header = request.headers
        self.parser.add_argument('userID', type=int)
        self.parser.add_argument('username', type=str)
        self.parser.add_argument('userEmail', type=str)


    #查询
    @auth_token
    def get(self, headers):
        #title必须大于5个字
        #文件内容模板
        #sendMail("求职soopooo", "382853739@qq.com")
        data = self.parser.parse_args()

        #获得用户信息
        userInfo = QueryConductor(data).queryProcess()
        if not userInfo:
            userInfo = User.query.all()
        results = UserSchema().dump(userInfo, many=True).data
        for result in results:
            # list->dict
            # for i, k in enumerate(result):
            #     result = k

            #获得指定用户参与的所有项目信息
            result["userInvolvedProjectsID"] = []
            result["userInvolvedProjectsName"] = []
            result["userCanManageProjectsID"] = []
            result["userCanManageProjectsName"] = []
            user_projectInfo = userProject.query.filter_by(userID=result["userID"]).all()
            result_user_project = userProjectSchema().dump(user_projectInfo, many=True).data
            print(result_user_project)
            for r in result_user_project:
                r["projectName"] = session.query(Project).filter_by(projectID=r['projectID']).first().projectName
                result["userInvolvedProjectsID"].append(r["projectID"])
                result["userInvolvedProjectsName"].append(r["projectName"])
                if (r["userType"] == 1):
                    result["userCanManageProjectsID"].append(r["projectID"])
                    result["userCanManageProjectsName"].append(r["projectName"])

        if (data.get("userID")):
            return {"statusCode": "1", "user": results}
        else:
            return {"statusCode": "1", "users": results}
        # return {"statusCode": "1", 'users': results}

    #增加
    @auth_token
    def post(self, headers):
        print(headers['userID'])
        #需要判断该用户是否有增加新用户的权限
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        print(json_data)
        # data, errors = UserSchema().load(json_data, session=session)
        # if errors:
        #     return errors,422
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
        )
        session.add(user)
        session.commit()


        db.session.execute(
            userProject.__table__.insert(),
            [{"userID": user.userID, "projectID": json_data["userInvolvedProjectsID"][i], "userType": "2"} for i
             in range(len(json_data["userInvolvedProjectsID"]))]

        )
        db.session.commit()
        db.session.execute(
            userProject.__table__.insert(),
            [{"userID": user.userID, "projectID": json_data['userCanManageProjectsID'][i], "userType": "1"}for i
             in range(len(json_data["userCanManageProjectsID"]))]

        )
        db.session.commit()
        sendMail("新用户创建成功", user.userEmail,user.userRealName, user.username, user.password)
        return {"statusCode": "1"}

    #更新
    @auth_token
    def put(self, headers):
        json_data = request.get_json(force=True)
        data_user_id = json_data['userID']
        update_user = session.query(User).filter_by(userID=data_user_id)
        update_json = json_data.copy()
        update_json.pop("userInvolvedProjectsID")
        update_json.pop("userCanManageProjectsID")

        print(update_json)
        update_user.update(update_json)
        session.query(userProject).filter(userProject.userID==data_user_id).delete()
        # session.delete(del_by_id)
        #更新方法，变量json_data中的所有数据
        # for k in json_data:
        #     update_user.update({k:json_data[k]})

        session.commit()

        db.session.execute(
            userProject.__table__.insert(),
            [{"userID": data_user_id, "projectID": json_data["userInvolvedProjectsID"][i], "userType": "2"} for i
             in range(len(json_data["userInvolvedProjectsID"]))]

        )
        db.session.commit()
        db.session.execute(
            userProject.__table__.insert(),
            [{"userID": data_user_id, "projectID": json_data['userCanManageProjectsID'][i], "userType": "1"} for i
             in range(len(json_data["userCanManageProjectsID"]))]

        )
        db.session.commit()

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