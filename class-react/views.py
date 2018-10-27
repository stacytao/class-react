from flask import Blueprint, g, render_template, request, redirect, session, url_for
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc
from . import util
from .model import *
bp = Blueprint("views", __name__)

TEXT = util.get_TEXT()
EMOJIS = util.get_EMOJIS()

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(user_id=user_id).first()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("views.login_user", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@bp.route("/")
def index():
    values = {
        "thumbsUp": 0,
        "thumbsDown": 0,
        "slowDown": 0,
        "volume": 0,
        "confused": 0,
        "hand": 0
    }

    most_popular = []
    count = 0
    for user in User.query.all():
        active_reaction = user.active_reaction
        if active_reaction and active_reaction.message != "🚫":
            emoji = active_reaction.message
            values[EMOJIS[emoji]] += 1
            if values[EMOJIS[emoji]] > count:
                count = values[EMOJIS[emoji]]
                most_popular = [TEXT[EMOJIS[emoji]]]
            elif values[EMOJIS[emoji]] == count:
                most_popular.append(TEXT[EMOJIS[emoji]])
    if count == 0:
        most_popular = ["🚫 None"]

    return render_template("home/class.html", values=values, popular=most_popular, popular_count=count)


@bp.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('home/404.html'), 404


###########
#  USERS  #
###########
@bp.route("/register", methods=["POST", "GET"])
def register_user():
    registration_error = False
    errors = {
        "username": None,
        "password": None
    }

    if request.method == "POST" and "form-button" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]

        user_exists = User.query.filter_by(username=username).count() > 0
        if user_exists is True:
            registration_error = True
            errors["username"] = "Username already exists. Please choose another one."

        if registration_error:
            return render_template("/user/register.html", error=errors)

        util.add_to_user_table(username, generate_password_hash(password), name)
        return redirect(url_for("views.login_user"))

    return render_template("/user/register.html")


@bp.route("/login", methods=["POST", "GET"])
def login_user():
    login_error = False
    errors = {
        "username": None,
        "password": "Hello"
    }

    if request.method == "POST" and "form-button" in request.form:
        username = request.form["username"]
        password = request.form["password"]

        users = User.query.filter_by(username=username)
        user = None
        if users.count() == 0:
            login_error = True
            errors["username"] = "Username doesn't exist. Please check your spelling."
        else:
            user = users.first()
            if not check_password_hash(user.password, password):
                login_error = True
                errors["password"] = "Incorrect password. Please try again."

        if login_error:
            return render_template("/user/login.html", error=errors)

        session.clear()
        session["user_id"] = user.user_id
        session["user_name"] = user.user_name
        return redirect(request.args.get("next") or url_for("views.index"))

    return render_template("/user/login.html")


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.index'))


@bp.route("/react")
@login_required
def profile():
    active_reaction = User.query.filter_by(user_id=session.get("user_id")).first().active_reaction
    reaction = "🚫 None"
    if active_reaction:
        reaction = TEXT[EMOJIS[active_reaction.message]]
    msgs = History.query.filter_by(author_id=session.get("user_id")).order_by(desc(History.timestamp)).limit(5).all()
    return render_template("home/profile.html", messages=msgs, reaction=reaction)
