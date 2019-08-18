from model.db import db, ma
#from marshmallow import Schema, fields, pre_load, validate
from marshmallow_sqlalchemy import ModelSchema


class Study(db.Model):

    __tablename__ = "study"
    study_id = db.Column(db.Integer, primary_key=True, autoincrement = True, unique=True)
    name = db.Column(db.String(255))
    status_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    description  = db.Column(db.String(255))
    plan_start_date = db.Column(db.DateTime)
    plan_end_date = db.Column(db.DateTime)



    def __init__(self, name ,status_id, user_id, description, plan_start_date, plan_end_date):
        self.name = name
        self.status_id = status_id
        self.user_id = user_id
        self.description = description
        self.plan_start_date = plan_start_date
        self.plan_end_date = plan_end_date


    def __repr__(self):
        return '<Sop %r>' % self.sop_id

class StudySchema(ModelSchema):
        class Meta:
            model = Study