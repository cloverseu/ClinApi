from model.db import db, ma
from marshmallow import Schema, fields, pre_load, validate
from marshmallow_sqlalchemy import ModelSchema


class User(db.Model):

    __tablename__ = "user"
    userID = db.Column(db.Integer, primary_key=True, autoincrement = True, unique=True)
    username = db.Column(db.String(255))
    userRealName = db.Column(db.String(255))
    password = db.Column(db.String(255))
    userEmail = db.Column(db.String(255))
    isAdmin = db.Column(db.Boolean)
    userAccountStatus = db.Column(db.String)
    userLastLoginTime = db.Column(db.DateTime)

    def __init__(self, username, userRealName, password, userEmail, isAdmin, userAccountStatus, userLastLoginTime):
        self.username = username
        self.userRealName = userRealName
        self.password = password
        self.userEmail = userEmail
        self.isAdmin = isAdmin
        self.userAccountStatus =  userAccountStatus
        self.userLastLoginTime = userLastLoginTime


    def __repr__(self):
        return '<User %r>' % self.userID

# class UserSchema(ModelSchema):
#         class Meta:
#             model = User

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
class UserSchema(ModelSchema):
        class Meta:
            model = User

#
#
#
# class UserSchema(ma.Schema):
#     username = fields.String(required=True, dump_only=True)
#     userRealName = fields.String(required=True, dump_only=True)
#     password = fields.String(required=True, dump_only=True)
#     userEmail = fields.String(required=True, dump_only=True)
#     isAdmin = fields.Boolean()
#     userAccountStatus = fields.Boolean()
    # userLastLoginTime = fields.DateTime(required=False)
