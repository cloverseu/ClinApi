from model.db import db, ma
#from marshmallow import Schema, fields, pre_load, validate
from marshmallow_sqlalchemy import ModelSchema


class sopFile(db.Model):

    __tablename__ = "sop"
    sop_id = db.Column(db.Integer, primary_key=True, autoincrement = True, unique=True)
    sop_name = db.Column(db.String(255))
    study_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    sop_description  = db.Column(db.String(255))
    sop_date_create = db.Column(db.DateTime)



    def __init__(self, sop_name ,study_id, user_id, sop_description, sop_date_create):
        self.sop_name = sop_name
        self.study_id = study_id
        self.user_id = user_id
        self.sop_description = sop_description
        self.sop_date_create = sop_date_create


    def __repr__(self):
        return '<Sop %r>' % self.sop_id

class sopFileSchema(ModelSchema):
        class Meta:
            model = sopFile