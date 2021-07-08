from flask import Flask
from db import initialize_db
from models import Notification

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] ={'host': 'mongodb://mongodb/db', 'port':27017}
initialize_db(app)

@app.route('/notifications')
def list_notification():
    data = Notification.objects.all().to_json()
    return data

@app.route('/notifications/:id')
def get_notification():
    data = Notification.objects.filter(id=id).to_json()
    return data
