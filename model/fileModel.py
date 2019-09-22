from model.db import db, ma
#from marshmallow import Schema, fields, pre_load, validate
from marshmallow_sqlalchemy import ModelSchema


class File(db.Model):

    __tablename__ = "file"
    fileID = db.Column(db.Integer, primary_key=True, autoincrement = True, unique=True)
    fileName = db.Column(db.String(255))
    fileDescription = db.Column(db.String)
    fileBelongedToTaskID = db.Column(db.Integer)
    fileBelongedToProjectID = db.Column(db.Integer)
    fileCreateDate = db.Column(db.DateTime)
    fileCreatorID = db.Column(db.Integer)
    fileStatus = db.Column(db.String(255))
    fileRemoveDate = db.Column(db.DateTime)
    fileRemoveExecutorID = db.Column(db.Integer)
    fileDeleteDate = db.Column(db.DateTime)
    fileDeleteExecutorID = db.Column(db.Integer)
    fileDownloadURL = db.Column(db.String(255))




    def __init__(self,fileName , fileDescription , fileBelongedToTaskID ,fileBelongedToProjectID ,fileCreateDate ,
                    fileCreatorID ,fileStatus , fileRemoveDate , fileRemoveExecutorID ,fileDeleteDate , fileDeleteExecutorID ,
                    fileDownloadURL):
        self.fileName = fileName
        self.fileDescription = fileDescription
        self.fileBelongedToTaskID = fileBelongedToTaskID
        self.fileBelongedToProjectID = fileBelongedToProjectID
        self.fileCreateDate = fileCreateDate
        self.fileCreatorID = fileCreatorID
        self.fileStatus = fileStatus
        self.fileRemoveDate = fileRemoveDate
        self.fileRemoveExecutorID = fileRemoveExecutorID
        self.fileDeleteDate = fileDeleteDate
        self.fileDeleteExecutorID = fileDeleteExecutorID
        self.fileDownloadURL = fileDownloadURL


def __repr__(self):
        return '<file %r>' % self.fileID

class FileSchema(ModelSchema):
        class Meta:
            model = File


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