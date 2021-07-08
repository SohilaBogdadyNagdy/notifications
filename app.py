import json
from flask import Flask, request, jsonify

from db import initialize_db
from models import Notification, User, NotificationLog

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] ={'host': 'mongo', 'port':27017}
initialize_db(app)

@app.route('/notifications')
def list_notification():
    data = Notification.objects.all().to_json()
    return jsonify({'data': data}), 200 

@app.route('/notifications/<id>')
def get_notification(id):
    data = Notification.objects.filter(id=id).to_json()
    return jsonify({'data': data}), 200

@app.route('/notification', methods=['POST'])
def post_notification():
    try:
        data = json.loads(request.data)
        notification = Notification(**data).save()
        return jsonify({'data': notification}), 201
    except BaseException as e:
        print(e)
        return e.message, 400


@app.route('/users', methods=['POST'])
def post_user():
    try:
        data = json.loads(request.data)
        user = User(**data).save()
        return jsonify({'data': user}), 201
    except BaseException as e:
        print(e)
        return e.message, 400


@app.route('/send/<id>', methods=['POST'])
def send(id):
    try:
        userIds = json.loads(request.data)
        notification = Notification.objects.filter(id=id).to_json()
        if not notification:
            return jsonify({
            "message": "BAD REQUEST",
            "success": False
        }), 400
        ### Call Send Notification ###
        log = {
            "notificationId": id,
            "userIds": userIds
        }
        NotificationLog(**log).save()
        return jsonify({
            "message": "Send Successfully",
            "success": True
        }), 200
    except BaseException as e:
        print(e)
        return e.message, 400


