from flask import Flask
from db import initialize_db
from models import Notification

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] ={'host': 'mongodb://localhost/db'}

initialize_db(app)

@app.route('/')
def send_notification():
    objs = Notification.objects.to_json()
    return objs

@app.route('/send')
def send_notification():
    obj = Notification.objects.to_json()
    return obj