#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author:    xurongzhong#126.com wechat:pythontesting qq:37391319
# CreateDate: 2018-1-10

import os

# You need to replace the next values with the appropriate values for your configuration
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:123456@localhost:5432/trial"

#mail config
MAIL_SERVER = "smtp.163.com"
MAIL_PORT =  25
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = "interclin@163.com"
MAIL_PASSWORD = "intercli666dd"
