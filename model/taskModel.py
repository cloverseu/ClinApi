from model.db import db, ma
#from marshmallow import Schema, fields, pre_load, validate
from marshmallow_sqlalchemy import ModelSchema




class Task(db.Model):

    __tablename__ = "task"
    taskID = db.Column(db.Integer, primary_key=True, autoincrement = True, unique=True)
    taskName =  db.Column(db.String(255))
    taskBelongedToProjectID =   db.Column(db.Integer)
    #belongedToTrialName = db.Column(db.String(255))
    taskCreatorID = db.Column(db.Integer)
    #taskCreatorName = db.Column(db.String(255))
    taskCreatedTime = db.Column(db.DateTime)
    taskExecutorID = db.Column(db.Integer)
    #taskExecutorName = db.Column(db.String(255))
    taskReceivedStatus = db.Column(db.String)
    taskDueTime = db.Column(db.DateTime)
    taskProgress = db.Column(db.Integer)
    taskCompletedStatus = db.Column(db.String)
    taskDescription = db.Column(db.String)
    taskActualCompletedTime = db.Column(db.DateTime)
    taskBelongedToProjectName = db.Column(db.String)
    taskExecutorRealName = db.Column(db.String)


    def __init__(self, taskName ,taskBelongedToProjectID,
                 taskCreatedTime, taskCreatorID, taskExecutorID,  taskReceivedStatus, taskDueTime,
                 taskProgress, taskCompletedStatus, taskDescription ,taskActualCompletedTime, taskBelongedToProjectName, taskExecutorRealName):
        self.taskName = taskName
        self.taskBelongedToProjectID = taskBelongedToProjectID
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
        self.taskDescription = taskDescription
        self.taskActualCompletedTime = taskActualCompletedTime
        self.taskBelongedToProjectName = taskBelongedToProjectName
        self.taskExecutorRealName = taskExecutorRealName

    def __repr__(self):
        return '<Task %r>' % self. taskID

class TaskSchema(ModelSchema):
        class Meta:
            model = Task


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
