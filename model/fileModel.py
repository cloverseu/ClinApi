from model.db import db



class Auditlog(db.Model):
    audit_id = db.Column(db.Integer, primary_key=True, autoincrement = True, unique=True)
    user_id = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    module= db.Column(db.String(60))
    action = db.Column(db.String(30))


    def __init__(self, user_id, create_date, module, action):
        self.user_id = user_id
        self.create_date = create_date
        self.module = module
        self.action = action

    def __repr__(self):
        return '<User %r>' % self.audit_id