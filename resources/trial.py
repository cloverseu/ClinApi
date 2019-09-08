from flask import request
from flask_restful import Resource, reqparse
from  model.trialModel import Trial, TrialSchema
from  model.db import db, session
import datetime
from  common.queryByItem import QueryConductor
from common.util import auth_token



class TrialResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('trialID', type=int)
        self.parser.add_argument('trialCreatorID', type=int)

        # parser.add_argument('file', type=FileStorage, location="files")
        # parser.add_argument('sop_name', type=str)
        # parser.add_argument('sop_description', type=str)

    #查询
    @auth_token
    def get(self, headers):
        data = self.parser.parse_args()
        # data_trial_id = data.get('trialID')
        # data_user_id = data.get('trialCreatorID')
        # if (data_trial_id or data_user_id):
        #     studyInfo = Trial.query.filter_by(trialCreatorID=str(data_user_id))
        # else:
        #     studyInfo = Trial.query.all()
        studyInfo = QueryConductor(data).queryProcess()
        if not studyInfo:
            studyInfo = Trial.query.all()
        result = TrialSchema().dump(studyInfo, many=True).data
        return {'message':'success', 'trialInfo':result}

    #增加(这部分是否可以重复利用)
    @auth_token
    def post(self, headers):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        print(json_data)
        #接收的日期格式为2014-08-11T05:26:03.869245
        data, errors = TrialSchema().load(json_data, session=session)
        if errors:
            return errors,422
        name = Trial.query.filter_by(trialName=json_data['trialName']).first()
        if name:
            return {'message': 'name already exists'}, 400

        #变量如果没有会怎样,需要指定阶段文件？

        trial = Trial(
            trialName = json_data['trialName'],
            trialStage = json_data['trialStage'],
            trialBriefIntroduction = json_data['trialBriefIntroduction'],
            trialCreatorID = json_data['trialCreatorID'],
            trialCreatedTime = json_data['trialCreatedTime'],
            trialExpectedStartTime = json_data['trialExpectedStartTime'],
            trialActualStartTime = json_data['trialActualStartTime'],
            trialExpectedEndTime = json_data['trialExpectedEndTime'],
            trialActualEndTime = json_data['trialActualEndTime'],
            trialSponsor = json_data['trialSponsor'],
            trialInvestigator = json_data['trialInvestigator'],
            trialMonitor = json_data['trialMonitor'],
            trialStatistician = json_data['trialStatistician']
        )
        session.add(trial)
        session.commit()

        return {'message': 'success','trialID': trial.trialID}

    #更新
    @auth_token
    def put(self, headers):
        data = parser.parse_args()
        data_trial_id = data.get('trialID')
        update_trial = session.query(Trial).filter_by(trialID=data_trial_id).first()
        update_trial.trialSponsor =  data.get('trialSponsor')
        session.commit()

        return {'message': 'success'}

    #删除
    @auth_token
    def delete(self, headers):
        data = parser.parse_args()
        data_trial_id = data.get('trialID')
        del_by_id = session.query(Trial).filter_by( trialID = data_trial_id).first()
        session.delete(del_by_id)
        session.commit()

        return { 'message':'success'}


