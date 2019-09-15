from model.db import db, ma
#from marshmallow import Schema, fields, pre_load, validate
from marshmallow_sqlalchemy import ModelSchema


class Project(db.Model):

    __tablename__ = "project"
    projectID = db.Column(db.Integer, primary_key=True, autoincrement = True, unique=True)
    projectName =  db.Column(db.String(255))
    projectStage =  db.Column(db.Integer)
    projectBriefIntroduction = db.Column(db.String(255))
    projectCreatorID = db.Column(db.Integer)
    projectCreatedTime = db.Column(db.DateTime)
    projectExpectedStartTime = db.Column(db.DateTime)
    projectActualStartTime = db.Column(db.DateTime)
    projectExpectedEndTime = db.Column(db.DateTime)
    projectActualEndTime = db.Column(db.DateTime)
    projectSponsor = db.Column(db.String(255))
    projectInvestigator = db.Column(db.String(255))
    projectMonitor = db.Column(db.String(255))
    projectStatistician = db.Column(db.String(255))

    #u_account = db.relationship('user_project', backref='project_info', lazy='dynamic')



    def __init__(self, projectName ,projectStage, projectBriefIntroduction, projectCreatorID, projectCreatedTime, projectExpectedStartTime,
                 projectActualStartTime, projectExpectedEndTime, projectActualEndTime, projectSponsor, projectInvestigator,
                 projectMonitor, projectStatistician):
        self.projectName = projectName
        self.projectStage = projectStage
        self.projectBriefIntroduction = projectBriefIntroduction
        self.projectCreatorID = projectCreatorID
        self.projectCreatedTime = projectCreatedTime
        self.projectExpectedStartTime = projectExpectedStartTime
        self.projectActualStartTime = projectActualStartTime
        self.projectExpectedEndTime = projectExpectedEndTime
        self.projectActualEndTime = projectActualEndTime
        self.projectSponsor = projectSponsor
        self.projectInvestigator = projectInvestigator
        self.projectMonitor = projectMonitor
        self.projectStatistician = projectStatistician


    def __repr__(self):
        return '<Project %r>' % self.projectID

class ProjectSchema(ModelSchema):
        class Meta:
            model = Project


#     projectID: TRIAL001,
#     projectName: 狂犬1针,
#     projectStage: 现眼包些着,
#     projectBriefIntroduction: 段处子件得特下百技业华日和志存相十长划放定将维如位历段身教命力风天引参头产理单两将近每和京号当性每见酸状员。,
#     projectCreatorID :1
#     projectCreatedTime: 1986-05-22 17:04:07,
#     projectExpectedStartTime: 1975-02-11 06:38:09,
#     projectActualStartTime: 1974-06-04 17:16:06,
#     projectExpectedEndTime: 2010-02-01 10:41:16,
#     projectActualEndTime: 2003-10-13 08:24:39,
#     projectSponsor: 革化解区温利着你别口关听,
#     projectInvestigator: 东员提步习资质很利,
#     projectMonitor: 张改省法积社达中包三持给它除,
#     projectStatistician: 但变我龙动没是江次术年接目事