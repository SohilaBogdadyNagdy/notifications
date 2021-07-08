import json
from flask import Flask

from db import initialize_db
from models import Notification

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] ={'host': 'mongo', 'port':27017}
initialize_db(app)

@app.route('/notifications')
def list_notification():
    data = Notification.objects.all().to_json()
    return data

@app.route('/notifications/:id')
def get_notification():
    print("dtaaaaaaaaaaa22222")
    data = Notification.objects.filter(id=id).to_json()
    return data

@app.route('/notification', methods=['POST'])
def post_notification():
    data = json.loads(request.data)
    return '', 204
