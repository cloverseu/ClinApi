from model.db import db, ma
#from marshmallow import Schema, fields, pre_load, validate
from marshmallow_sqlalchemy import ModelSchema


class taskFiles(db.Model):

    __tablename__ = "taskFiles"
    fileID = db.Column(db.Integer, primary_key=True, autoincrement = True, unique=True)
    belongedToTaskID = db.Column(db.Integer)
    fileName = db.Column(db.String(255))
    createDate = db.Column(db.DateTime)
    creatorID = db.Column(db.Integer)
    #creatorName = db.Column(db.String(255))
    description = db.Column(db.String(255))
    deleteDate = db.Column(db.DateTime)
    deleteExecutorID = db.Column(db.Integer)
    #deleteExecutorName = db.Column(db.String(255))
    downloadURL = db.Column(db.String(255))



    def __init__(self,belongedToTaskID, fileName, createDate, creatorID,
                 description, deleteDate, deleteExecutorID, downloadURL
                 ):
        self.belongedToTaskID = belongedToTaskID
        self.fileName = fileName
        self.createDate = createDate
        self.creatorID = creatorID
        #self.creatorName = creatorName
        self.description = description
        self.deleteDate = deleteDate
        self.deleteExecutorID = deleteExecutorID
        #self.deleteExecutorName = deleteExecutorName
        self.downloadURL = downloadURL


    def __repr__(self):
        return '<Sop %r>' % self.fileID

class taskFileSchema(ModelSchema):
        class Meta:
            model = taskFiles


 # "fileID": "FILE001",
 #      "belongedToTaskID": "TASK001",
 #      "fileName": "DMP-SOP-V1.0",
 #      "createDate": "2019-08-11",
 #      "creatorID": "USER001",
 #      "creatorName": "刘沛",
 #      "description": "版本已更新，请勿使用！",
 #      "deleteDate": "2019-08-11",
 #      "deleteExecutorID": "USER001",
 #      "deleteExecutorName": "刘沛",
 #      "downloadURL": ""