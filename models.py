from flask.app import Flask
from db import db

class Notification(db.Document):
    type = db.StringField(required=True, unique=True)
    message = db.StringField(required=True, unique=True)
    createdAt = db.DateField()

class User(db.Document):
    name = db.StringField(required=True)
    lang = db.StringField(required=True)

class NotificationLog(db.Document):
    notificationId = db.StringField(required=True)
    userIds = db.ListField(required=True)