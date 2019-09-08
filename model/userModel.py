from model.db import db, ma
#from marshmallow import Schema, fields, pre_load, validate
from marshmallow_sqlalchemy import ModelSchema


class User(db.Model):

    __tablename__ = "user"
    userID = db.Column(db.Integer, primary_key=True, autoincrement = True, unique=True)
    username = db.Column(db.String(255))
    userRealName = db.Column(db.String(255))
    password = db.Column(db.String(255))


    def __init__(self, username, userRealName, password):
        self.username = username
        self.userRealName = userRealName
        self.password = password


    def __repr__(self):
        return '<Sop %r>' % self.userID

class UserSchema(ModelSchema):
        class Meta:
            model = User

# class User(db.Model):
#
#     __tablename__ = "user"
#     user_id = db.Column(db.Integer, primary_key=True, autoincrement = True, unique=True)
#     username = db.Column(db.String(120), unique=True)
#     password = db.Column(db.String(120))
#     email = db.Column(db.String(120))
#     is_admin = db.Column(db.Integer)
#     can_createTrail = db.Column(db.Integer)
#     can_createSop = db.Column(db.Integer)
#     date_create = db.Column(db.DateTime)
#     is_active = db.Column(db.Integer)
#
#
#     def __init__(self, username, password, email, date_create, is_admin=0, can_createTrail=0, can_createSop=0, is_active=1):
#         self.username = username
#         self.password = password
#         self.email = email
#         self.is_admin = is_admin
#         self.can_createTrail = can_createTrail
#         self.can_createSop = can_createSop
#         self.date_create =   date_create
#         self.is_active = is_active
#
#
#     def __repr__(self):
#         return '<User %r>' % self.user_id
#
# # class UserSchema(ModelSchema):
# #         class Meta:
# #             model = User
#
#
#
#
# class UserSchema(ma.Schema):
#     user_id = fields.Integer(dump_only=True)
#     username = fields.String(required=True, dump_only=True)
#     password = fields.String(required=True)
#     email = fields.String()
#     #此处需要设置默认值
#     is_admin = fields.Integer()
#     can_createTrail = fields.Integer()
#     can_createSop = fields.Integer()
#     #date_create = fields.DateTime()
#     is_active = fields.Integer()