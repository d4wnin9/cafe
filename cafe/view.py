import flask
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash

from cafe.database import db
from cafe.user import LoginUser

# passwords are stored in plain text

def index():
    if flask_login.current_user.is_authenticated:
        return flask.render_template("index.html")
    return 'Login -> <a href="/login">/login</a>'

def register():
    if flask.request.method == 'GET':
        return flask.render_template('register.html')

    username = flask.request.form.get('username')
    try:
        user = LoginUser.query.filter(LoginUser.username == username).one_or_none()
        if user == None:
            user = LoginUser()
            user.username = username
            user.password = generate_password_hash(flask.request.form.get('password'))
            db.session.add(user)
            db.session.commit()
            flask_login.login_user(user, remember=True)
            return flask.redirect(flask.url_for('index'))
        else:
            flask.render_template('register.html', error='すでに使われている名前です')
    except Exception as e:
        return flask.render_template('register.html', error=e)

def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    username = flask.request.form.get('username')
    try:
        user = LoginUser.query.filter(LoginUser.username == username).one_or_none()
        if user == None:
            return flask.render_template('login.html', error='指定のユーザーは存在しません')
        elif not check_password_hash(user.password, flask.request.form.get('password')):
            return flask.render_template('login.html', error='パスワードが間違っています')
        else:
            flask_login.login_user(user, remember=True)
            return flask.redirect(flask.url_for('index'))
    except Exception as e:
        return flask.render_template('login.html', error=e)

@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('index'))
