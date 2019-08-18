from model.db import db, ma
#from marshmallow import Schema, fields, pre_load, validate
from marshmallow_sqlalchemy import ModelSchema


class Trial(db.Model):

    __tablename__ = "trial"
    trialID = db.Column(db.Integer, primary_key=True, autoincrement = True, unique=True)
    trialName =  db.Column(db.String(255))
    trialStage =  db.Column(db.Integer)
    trialBriefIntroduction = db.Column(db.String(255))
    trialCreatorID = db.Column(db.Integer)
    trialCreatedTime = db.Column(db.DateTime)
    trialExpectedStartTime = db.Column(db.DateTime)
    trialActualStartTime = db.Column(db.DateTime)
    trialExpectedEndTime = db.Column(db.DateTime)
    trialActualEndTime = db.Column(db.DateTime)
    trialSponsor = db.Column(db.String(255))
    trialInvestigator = db.Column(db.String(255))
    trialMonitor = db.Column(db.String(255))
    trialStatistician = db.Column(db.String(255))



    def __init__(self, trialName ,trialStage, trialBriefIntroduction, trialCreatorID, trialCreatedTime, trialExpectedStartTime,
                 trialActualStartTime, trialExpectedEndTime, trialActualEndTime, trialSponsor, trialInvestigator,
                 trialMonitor, trialStatistician):
        self.trialName = trialName
        self.trialStage = trialStage
        self.trialBriefIntroduction = trialBriefIntroduction
        self.trialCreatorID = trialCreatorID
        self.trialCreatedTime = trialCreatedTime
        self.trialExpectedStartTime = trialExpectedStartTime
        self.trialActualStartTime = trialActualStartTime
        self.trialExpectedEndTime = trialExpectedEndTime
        self.trialActualEndTime = trialActualEndTime
        self.trialSponsor = trialSponsor
        self.trialInvestigator = trialInvestigator
        self.trialMonitor = trialMonitor
        self.trialStatistician = trialStatistician


    def __repr__(self):
        return '<Sop %r>' % self.trialID

class TrialSchema(ModelSchema):
        class Meta:
            model = Trial


#     trialID: TRIAL001,
#     trialName: 狂犬1针,
#     trialStage: 现眼包些着,
#     trialBriefIntroduction: 段处子件得特下百技业华日和志存相十长划放定将维如位历段身教命力风天引参头产理单两将近每和京号当性每见酸状员。,
#     trialCreatorID :1
#     trialCreatedTime: 1986-05-22 17:04:07,
#     trialExpectedStartTime: 1975-02-11 06:38:09,
#     trialActualStartTime: 1974-06-04 17:16:06,
#     trialExpectedEndTime: 2010-02-01 10:41:16,
#     trialActualEndTime: 2003-10-13 08:24:39,
#     trialSponsor: 革化解区温利着你别口关听,
#     trialInvestigator: 东员提步习资质很利,
#     trialMonitor: 张改省法积社达中包三持给它除,
#     trialStatistician: 但变我龙动没是江次术年接目事