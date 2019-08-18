from model.db import db, ma
#from marshmallow import Schema, fields, pre_load, validate
from marshmallow_sqlalchemy import ModelSchema


class Tasks(db.Model):

    __tablename__ = "tasks"
    taskID = db.Column(db.Integer, primary_key=True, autoincrement = True, unique=True)
    taskName =  db.Column(db.String(255))
    belongedToTrialID =   db.Column(db.Integer)
    #belongedToTrialName = db.Column(db.String(255))
    taskCreatorID = db.Column(db.Integer)
    #taskCreatorName = db.Column(db.String(255))
    taskCreatedTime = db.Column(db.DateTime)
    taskExecutorID = db.Column(db.Integer)
    #taskExecutorName = db.Column(db.String(255))
    taskReceivedStatus = db.Column(db.Boolean)
    taskDueTime = db.Column(db.DateTime)
    taskProgress = db.Column(db.Integer)
    taskCompletedStatus = db.Column(db.Boolean)
    taskActualCompletedTime = db.Column(db.DateTime)


    def __init__(self, taskName ,belongedToTrialID,  taskCreatorID,
                 taskCreatedTime, taskExecutorID,  taskReceivedStatus, taskDueTime,
                 taskProgress, taskCompletedStatus, taskActualCompletedTime):
        self.taskName = taskName
        self.belongedToTrialID = belongedToTrialID
        #self.belongedToTrialName = belongedToTrialName
        self.taskCreatorID =taskCreatorID
        #self.taskCreatorName = taskCreatorName
        self.taskCreatedTime = taskCreatedTime
        self.taskExecutorID = taskExecutorID
        #self.taskExecutorName = taskExecutorName
        self.taskReceivedStatus = taskReceivedStatus
        self.taskDueTime = taskDueTime
        self.taskProgress = taskProgress
        self.taskCompletedStatus = taskCompletedStatus
        self.taskActualCompletedTime = taskActualCompletedTime


    def __repr__(self):
        return '<Sop %r>' % self. taskID

class TaskSchema(ModelSchema):
        class Meta:
            model = Tasks


 #      taskID: TASK001,
 #      taskName: 写DMP,
 #      belongedToTrialID: TRIAL001,
 #      belongedToTrialName: 狂犬1针,
 #      taskCreatorID: USER001,
 #      taskCreatorName: 刘沛,
 #      taskCreatedTime: 1998-06-11 23:07:21,
 #      taskExecutorID: USER003,
 #      taskExecutorName: 范扬,
 #      taskReceivedStatus: false,
 #      taskDueTime: 2013-11-30 13:23:51,
 #      taskProgress: 24,
 #      taskCompletedStatus: false,
 #      taskActualCompletedTime: 2005-06-20 19:12:56