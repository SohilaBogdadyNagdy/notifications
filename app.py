import time

import redis
from flask import Flask

app = Flask(__name__)

@app.route('/send')
def send_notification():
    return 'Hello World! I have been seen times.\n'