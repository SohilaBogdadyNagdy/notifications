import json
from flask_swagger import swagger
from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

from db import initialize_db
from models import Notification, User, NotificationLog

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] ={'host': 'mongo', 'port':27017}
initialize_db(app)


### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Notification"}
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
    ### end swagger specific ###

@app.route("/spec")
def spec():

    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "My API"
    return jsonify(swag)


@app.route('/notifications')
def list_notification():
    data = Notification.objects.all().to_json()
    return jsonify({'data': data}), 200 

@app.route('/notifications/<id>')
def get_notification(id):
    data = Notification.objects.filter(id=id).to_json()
    return jsonify({'data': data}), 200

@app.route('/notifications', methods=['POST'])
def post_notification():
    """
        Create a new notification
        ---
        tags:
          - notifications
        definitions:
          - schema:
              id: Notification
              properties:
                message:
                 type: string
                 description: the notification message
                type:
                 type: string
                 description: the notification type
        parameters:
          - in: body
            name: body
            schema:
              id: Notification
              required:
                - type
                - message
              properties:
                type:
                  type: string
                  description: notification type
                message:
                  type: string
                  description: notification message
        responses:
          201:
            description: Notification created
        """
    try:
        data = json.loads(request.data)
        notification = Notification(**data).save()
        return jsonify({'data': notification}), 201
    except BaseException as e:
        print(e)
        return e.message, 400


@app.route('/users', methods=['POST'])
def post_user():
    """
        Create a new user
        ---
        tags:
          - users
        definitions:
          - schema:
              id: User
              properties:
                name:
                 type: string
                 description: the user name
                lang:
                 type: string
                 description: the user language
        parameters:
          - in: body
            name: body
            schema:
              id: User
              required:
                - lang
                - name
              properties:
                lang:
                  type: string
                  description: user language
                name:
                  type: string
                  description: name for user
        responses:
          201:
            description: User created
        """
    try:
        data = json.loads(request.data)
        user = User(**data).save()
        return jsonify({'data': user}), 201
    except BaseException as e:
        print(e)
        return e.message, 400


@app.route('/notification/send/<id>', methods=['POST'])
def send(id):
    """
        Send a new notification
        ---
        tags:
          - send 
        parameters:
          - in: body
            name: body
            schema:
              id: Send
              required:
                - userIds
              properties:
                userIds:
                  type: string
                  description: list of user ids
                
        responses:
          200:
            description: send successfully
        """
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


