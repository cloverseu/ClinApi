from model.db import db, ma
#from marshmallow import Schema, fields, pre_load, validate
from marshmallow_sqlalchemy import ModelSchema


class Template(db.Model):

    __tablename__ = "template"
    templateID = db.Column(db.Integer, primary_key=True, autoincrement = True, unique=True)
    templateName = db.Column(db.String(255))
    templateDescription = db.Column(db.String)
    templateCreateDate = db.Column(db.DateTime)
    templateCreatorID = db.Column(db.Integer)
    templateStatus = db.Column(db.String(255))
    templateRemoveDate = db.Column(db.DateTime)
    templateRemoveExecutorID = db.Column(db.Integer)
    templateDeleteDate = db.Column(db.DateTime)
    templateDeleteExecutorID = db.Column(db.Integer)
    templateDownloadURL = db.Column(db.String(255))
    templateCreatorName = db.Column(db.String(255))




    def __init__(self,templateName , templateDescription ,templateCreateDate ,
                    templateCreatorID ,templateStatus , templateRemoveDate , templateRemoveExecutorID ,templateDeleteDate , templateDeleteExecutorID ,
                    templateDownloadURL, templateCreatorName):
        self.templateName = templateName
        self.templateDescription = templateDescription
        self.templateCreateDate = templateCreateDate
        self.templateCreatorID = templateCreatorID
        self.templateStatus = templateStatus
        self.templateRemoveDate = templateRemoveDate
        self.templateRemoveExecutorID = templateRemoveExecutorID
        self.templateDeleteDate = templateDeleteDate
        self.templateDeleteExecutorID = templateDeleteExecutorID
        self.templateDownloadURL = templateDownloadURL
        self.templateCreatorName = templateCreatorName


def __repr__(self):
        return '<template %r>' % self.templateID

class TemplateSchema(ModelSchema):
        class Meta:
            model = Template


 # "templateID": "FILE001",
 #      "belongedToTaskID": "TASK001",
 #      "templateName": "DMP-SOP-V1.0",
 #      "createDate": "2019-08-11",
 #      "creatorID": "USER001",
 #      "creatorName": "刘沛",
 #      "description": "版本已更新，请勿使用！",
 #      "deleteDate": "2019-08-11",
 #      "deleteExecutorID": "USER001",
 #      "deleteExecutorName": "刘沛",
 #      "downloadURL": ""