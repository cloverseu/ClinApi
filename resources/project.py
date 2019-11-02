from flask import request
from flask_restful import Resource, reqparse
from  model.projectModel import Project, ProjectSchema
from model.user_projectModel import userProject
from model.userModel import User,UserSchema
from model.user_projectModel import userProject, userProjectSchema
from  model.db import db, session
import time
from  common.queryByItem import QueryConductor
from common.util import auth_token



class ProjectResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('projectID', type=int)
        # self.parser.add_argument('projectCreatorID', type=int)
        self.parser.add_argument('projectName', type=str)
        self.parser.add_argument('projectInvestigatorName', type=str)
        self.parser.add_argument('projectSponsor', type=str)
        self.parser.add_argument('projectInvolvedUserRealName', type=str)
        self.parser.add_argument('projectCreatedYearMonth', type=str)
        self.parser.add_argument('projectStage', type=str)
        self.parser.add_argument('projectCreatedTime')


        # parser.add_argument('file', type=FileStorage, location="files")
        # parser.add_argument('sop_name', type=str)
        # parser.add_argument('sop_description', type=str)

    #查询
    @auth_token
    def get(self, headers):
        print(headers)
        data = self.parser.parse_args()
        print(data)
        studyInfo = QueryConductor(data).queryProcess()
        if not studyInfo:
            studyInfo = Project.query.all()
        results = ProjectSchema().dump(studyInfo, many=True)





        # projectID = None
        # for i, k in enumerate(result):
        #     projectID = k["projectID"]

        #传入的peojectID或者isAdmin
        if (headers["isAdmin"] or data.get("projectID")):
            for result in results:
                result["projectInvolvedUsersID"] = []
                result["projectInvolvedUsersName"] = []
                user_projectInfo = userProject.query.filter_by(projectID=result["projectID"]).all()
                result_user_project = userProjectSchema().dump(user_projectInfo, many=True)
                print("eee")
                print(result_user_project)
                if len(results)==1:
                    like_filters = {}
                    like_filters["projectID"] = result["projectID"]
                    like_filters["userType"] = 1
                    manager = userProject.query.filter_by(**like_filters)
                    print(manager.first())
                    if manager.first():
                        result["projectManagerName"] = session.query(User).filter_by(userID=manager.first().userID).first().username
                    for r in result_user_project:
                        r["username"] =  session.query(User).filter_by(userID=r["userID"]).first().username
                        if (r["userType"] == 2):
                            result["projectInvolvedUsersID"].append(r["userID"])
                            result["projectInvolvedUsersName"].append(r["username"])

        #传入userID
        else:
            results = []
            user_projectInfo = userProject.query.filter_by(userID=headers["userID"]).all()
            result_user_project = userProjectSchema().dump(user_projectInfo, many=True).data
            for i in result_user_project:
                studyInfo = Project.query.filter_by(projectID = i["projectID"])
                results.append(ProjectSchema().dump(studyInfo, many=True))


        # return { "statusCode": "1", 'project':results}
        if (data.get("projectID")):
            return {"statusCode": "1", "project": results}
        else:
            return {"statusCode": "1", "projects": results}

    #增加(这部分是否可以重复利用)
    @auth_token
    def post(self, headers):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        #接收的日期格式为2014-08-11T05:26:03.869245
        # data, errors = ProjectSchema().load(json_data, session=session)
        # if errors:
        #     return errors,422
        name = Project.query.filter_by(projectName=json_data['projectName']).first()
        if name:
            return {'message': 'name already exists'}, 400

        #变量如果没有会怎样,需要指定阶段文件？

        project = Project(
            projectName = json_data['projectName'],
            projectStage = json_data['projectStage'],
            projectBriefIntroduction = json_data['projectBriefIntroduction'],
            # projectCreatorID = json_data['projectCreatorID'],
            projectCreatedTime = time.ctime(time.time()),
            projectExpectedStartTime = json_data['projectExpectedStartTime'],
            projectActualStartTime = json_data['projectActualStartTime'],
            projectExpectedEndTime = json_data['projectExpectedEndTime'],
            projectActualEndTime = json_data['projectActualEndTime'],
            projectSponsor = json_data['projectSponsor'],
            projectInvestigator = json_data['projectInvestigator'],
            projectMonitor = json_data['projectMonitor'],
            projectStatistician = json_data['projectStatistician']
        )
        print(json_data)

        session.add(project)
        db.session.commit()
#         db.session.execute(
#             userProject.__table__.insert(),
#             [{"projectID":project.projectID , "userID": json_data["projectInvolvedUsersID"][i], "userType":"2"} for i in range(len(json_data["projectInvolvedUsersID"]))]
#
#         )
#         db.session.commit()
#         db.session.execute(
#             userProject.__table__.insert(),
#             [{"projectID": project.projectID, "userID": json_data['projectCreatorID'], "userType": "1"}
# ]
#
#         )
#         db.session.commit()
        return {'statusCode': '1','projectID': project.projectID}

    #更新，如果要修改则需要删掉原先的userproject中的关联重新添加
    @auth_token
    def put(self, headers):
        json_data = request.get_json(force=True)
        data_project_id = json_data['projectID']
        update_project = session.query(Project).filter_by(projectID=data_project_id)

        # update_project.projectSponsor =  data.get('projectSponsor')
        update_project.update(json_data)
        session.commit()

        return { "statusCode": "1"}

    #删除
    @auth_token
    def delete(self, headers):
        data = self.parser.parse_args()
        data_user_id = data.get('projectID')

        session.query(userProject).filter(userProject.projectID==data_user_id).delete()

        session.query(Project).filter(Project.projectID==data_user_id).delete()
        #del_by_projectID = Project.query.filter(Project.projectID==data_user_id).first()
        #db.session.delete(del_by_projectID)
        #session.delete(del_by_projectID)
        db.session.commit()

        return {"statusCode": "1"}


