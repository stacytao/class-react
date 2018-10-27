import os

from flask import Flask
from flask_socketio import SocketIO, send
from .model import db
from .views import bp
from .util import *


# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev'
)

app.config.from_pyfile('config.py', silent=True)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

app.register_blueprint(bp)
db.init_app(app)
try:
    init_db()
except:
    db.session.rollback()

# SocketIO
socketio = SocketIO(app)


@socketio.on('message')
def handleMessage(msg):
    datetime = util.get_timestamp(msg[3])
    message = History(message=msg[0], author_name=msg[1], author_id=msg[2], timestamp=datetime)
    
    db.session.add(message)
    db.session.commit()

    msg = {
        "message": message.message,
        "author_name": message.author_name,
        "author_id": message.author_id,
        "timestamp": str(message.timestamp)
    }

    send(msg, broadcast=True)


if __name__ == '__main__':
    socketio.run(app)
