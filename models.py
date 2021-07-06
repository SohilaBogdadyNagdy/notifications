from db import db

class Notification(db.Document):
    type = db.StringField(required=True, unique=True)
    text = db.ListField(db.StringField(), required=True)
