from flask import request
from flask_restful import Resource, reqparse
from  model.taskModel import Task, TaskSchema
from  model.userModel import User, UserSchema
from  model.projectModel import Project, ProjectSchema
from  model.db import db, session
from  common.queryByItem import QueryConductor
from common.util import auth_token
import time
from common.util import sendMail
from sqlalchemy import or_

class TaskResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('taskID', type=int)
        self.parser.add_argument('taskName', type=str)
        self.parser.add_argument('taskCreatorID', type=int)
        self.parser.add_argument('taskExecutorID', type=int)
        self.parser.add_argument('taskExecutorName', type=str)
        self.parser.add_argument('taskReceivedStatus', type=str)
        self.parser.add_argument('taskCompletedStatus', type=str)
        self.parser.add_argument('taskDescription', type=str)
        self.parser.add_argument('isAdminMode', type=str)
        # parser.add_argument('file', type=FileStorage, location="files")
        # parser.add_argument('sop_name', type=str)
        # parser.add_argument('sop_description', type=str)

    #查询
    @auth_token
    def get(self, headers):
        # print(dir(Tasks))
        data = self.parser.parse_args()
        # data.update({"taskExecutorID" : headers["userID"]})
        isAdminMode = data.get("isAdminMode")
        data.pop("isAdminMode")
        if isAdminMode:
            if (isAdminMode == "false"):
                cdt = {or_(Task.taskExecutorID ==  headers["userID"],Task.taskCreatorID ==  headers["userID"])}
            else:
                #isadmin做筛选时候是有问题的？？
                cdt = {Task.taskExecutorID > 0}
        else:
            cdt = {Task.taskExecutorID ==  headers["userID"]}
        tasksInfo = QueryConductor(data, cdt).queryProcess()
        # print(cdt)
        # tasksInfo = QueryConductor(data, cdt).queryProcess()
        # if not tasksInfo:
            # tasksInfo = Task.query.all()
        result = TaskSchema().dump(tasksInfo, many=True)
        for r in result:
            #r["taskBelongedToProjectName"] = session.query(Project).filter_by(projectID=r['taskBelongedToProjectID']).first().projectName
            r["taskCreatorName"] = session.query(User).filter_by(userID=r['taskCreatorID']).first().username
            r["taskCreatorRealName"] = session.query(User).filter_by(userID=r['taskCreatorID']).first().userRealName
            r["taskExecutorName"] = session.query(User).filter_by(userID=r['taskExecutorID']).first().username
        if (data.get("taskID")):
            return {"statusCode": "1", "task":result}
        else:
            return {"statusCode": "1", "tasks": result}
    #增加(这部分是否可以重复利用)
    @auth_token
    def post(self, headers):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        print(json_data)
        #接收的日期格式为2014-08-11T05:26:03.869245
        # data, errors = TaskSchema().load(json_data, session=session)
        # if errors:
        #     return errors,422
        name = Task.query.filter_by(taskName=json_data['taskName']).first()
        if name:
            return {'message': 'name already exists'}, 400

        #变量如果没有会怎样,需要指定阶段文件？
        taskBelongedToProjectName = session.query(Project).filter_by(projectID=json_data['taskBelongedToProjectID']).first().projectName
        taskExecutorRealName = session.query(User).filter_by(userID=headers['userID']).first().userRealName
        task = Task(
            taskName = json_data['taskName'],
            taskBelongedToProjectID = json_data['taskBelongedToProjectID'],
            #belongedToTrialName = json_data['belongedToTrialName'],
            taskCreatorID = headers['userID'],
            #taskCreatorName = json_data['taskCreatorName'],
            taskCreatedTime = time.strftime("%Y-%m-%d", time.localtime()),
            taskExecutorID = json_data['taskExecutorID'],
            #taskExecutorName = json_data['taskExecutorName'],
            taskReceivedStatus = json_data['taskReceivedStatus'],
            taskDueTime = json_data['taskDueTime'],
            taskProgress = json_data['taskProgress'],
            taskCompletedStatus = None,
            taskDescription = json_data['taskDescription'],
            taskActualCompletedTime = None,
            taskBelongedToProjectName = taskBelongedToProjectName,
            taskExecutorRealName = taskExecutorRealName
        )
        session.add(task)
        session.commit()

        executor = User.query.filter(User.userID==task.taskExecutorID).first()
        taskBelongedToProject = Project.query.filter(Project.projectID == task.taskBelongedToProjectID).first()
        sendMail("任务分配通知", executor.userEmail, executor.userRealName, taskBelongedToProject.projectName,task.taskName, task.taskDescription, task.taskDueTime.strftime("%Y-%m-%d"))

        return {"statusCode": "1","taskID": task.taskID}

    #更新
    @auth_token
    def put(self, headers):
        json_data = request.get_json(force=True)
        data_task_id = json_data['taskID']

        update_task = session.query(Task).filter_by(taskID=data_task_id)
        update_task.update(json_data)

        session.commit()

        return { "statusCode": "1"}

    #删除
    @auth_token
    def delete(self, headers):
        data = self.parser.parse_args()
        data_task_id = data.get('taskID')
        del_by_id = session.query(Task).filter_by( taskID = data_task_id).first()
        session.delete(del_by_id)
        session.commit()

        return {"statusCode": "1"}


