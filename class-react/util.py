from .model import *
import datetime


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
