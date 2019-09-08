from flask import request
from flask_restful import Resource, reqparse
from  model.tasksModel import Tasks, TaskSchema
from  model.userModel import User, UserSchema
from  model.trialModel import Trial, TrialSchema
from  model.db import db, session
from  common.queryByItem import QueryConductor
from common.util import auth_token
import datetime



class TasksResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('taskID', type=int)
        self.parser.add_argument('taskCreatorID', type=int)
        self.parser.add_argument('taskExecutorID', type=int)
        # parser.add_argument('file', type=FileStorage, location="files")
        # parser.add_argument('sop_name', type=str)
        # parser.add_argument('sop_description', type=str)

    #查询
    @auth_token
    def get(self, headers):
        # print(dir(Tasks))
        data = self.parser.parse_args()
        # data_trial_id = data.get('taskID')
        # print(data.keys())
        # print(list(data.keys())[1])
        # print('taskIDs' in data.keys())
        # data_user_id = data.get('taskCreatorID')
        # item = list(data.keys())
        # for i in item:
        #     if(data.get(i)):
        #         item = i
        # filters = {item:data.get(item)}
        # print(filters)
        # tasksInfo = Tasks.query.filter_by(**filters)
        # if (data_trial_id or data_user_id):
        #     tasksInfo = Tasks.query.filter_by(taskCreatorID=data_trial_id)
        # else:
        #     tasksInfo = Tasks.query.all()
        tasksInfo = QueryConductor(data).queryProcess()
        if not tasksInfo:
            tasksInfo = Tasks.query.all()
        result = TaskSchema().dump(tasksInfo, many=True).data
        for r in result:
            r["belongedToTrialName"] = session.query(Trial).filter_by(trialID=r['belongedToTrialID']).first().trialName
            r["taskCreatorName"] = session.query(User).filter_by(userID=r['taskCreatorID']).first().userName
            r["taskExecutorName"] = session.query(User).filter_by(userID=r['taskExecutorID']).first().userName
        return {'message':'success', 'tasksInfo':result}

    #增加(这部分是否可以重复利用)
    @auth_token
    def post(self, headers):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        print(json_data)
        #接收的日期格式为2014-08-11T05:26:03.869245
        data, errors = TaskSchema().load(json_data, session=session)
        if errors:
            return errors,422
        name = Tasks.query.filter_by(taskName=json_data['taskName']).first()
        if name:
            return {'message': 'name already exists'}, 400

        #变量如果没有会怎样,需要指定阶段文件？

        task = Tasks(
            taskName = json_data['taskName'],
            belongedToTrialID = json_data['belongedToTrialID'],
            #belongedToTrialName = json_data['belongedToTrialName'],
            taskCreatorID = json_data['taskCreatorID'],
            #taskCreatorName = json_data['taskCreatorName'],
            taskCreatedTime = json_data['taskCreatedTime'],
            taskExecutorID = json_data['taskExecutorID'],
            #taskExecutorName = json_data['taskExecutorName'],
            taskReceivedStatus = json_data['taskReceivedStatus'],
            taskDueTime = json_data['taskDueTime'],
            taskProgress = json_data['taskProgress'],
            taskCompletedStatus = json_data['taskCompletedStatus'],
            taskActualCompletedTime = json_data['taskActualCompletedTime']
        )
        session.add(task)
        session.commit()

        return {'message': 'success','taskID': task.taskID}

    #更新
    @auth_token
    def put(self, headers):
        data = parser.parse_args()
        data_task_id = data.get('taskID')

        update_task = session.query(Tasks).filter_by(taskID=data_task_id).update()

        Student.query.filter_by(s_id=3).update({'s_name': '娃哈哈'})
        update_task.taskSponsor =  data.get('taskSponsor')
        session.commit()

        return {'message': 'success'}

    #删除
    @auth_token
    def delete(self, headers):
        data = parser.parse_args()
        data_task_id = data.get('taskID')
        del_by_id = session.query(Tasks).filter_by( taskID = data_task_id).first()
        session.delete(del_by_id)
        session.commit()

        return { 'message':'success'}


