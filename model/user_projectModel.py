from model.db import db, ma
#from marshmallow import Schema, fields, pre_load, validate
from marshmallow_sqlalchemy import ModelSchema


class userProject(db.Model):

    __tablename__ = "user_project"
    userProjectID = db.Column(db.Integer, primary_key=True, autoincrement = True, unique=True)
    userID = db.Column(db.Integer)
    projectID = db.Column(db.Integer)
    userType = db.Column(db.Integer)


    def __init__(self, projectID, userID, userType):
        self.userID = userID
        self.projectID = projectID
        self.userType = userType



    def __repr__(self):
        return '<userProjectID %r>' % self.userProjectID

class userProjectSchema(ModelSchema):
        class Meta:
            model = userProject

