from .model import *
import datetime


TEXT = {
    "none": "🚫 None",
    "thumbsUp": "👍 Like/Yes",
    "thumbsDown": "👎 Dislike/No",
    "slowDown": "🐢 Slow Down",
    "volume": "📣 Speak Louder",
    "confused": "❓ Confused",
    "hand": "👋 Raised Hand"
}
EMOJIS = {
    "🚫": "none",
    "👍": "thumbsUp",
    "👎": "thumbsDown",
    "🐢": "slowDown",
    "📣": "volume",
    "❓": "confused",
    "👋": "hand"
}


def get_TEXT():
    return TEXT


def get_EMOJIS():
    return EMOJIS


def init_db():
    db.create_all()


def get_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


###########
#  USERS  #
###########
def add_to_user_table(username, pwhash, name):
    user = User(username=username, password=pwhash, user_name=name)
    db.session.add(user)
    db.session.commit()
