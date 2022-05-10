import flask
import flask_login

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
    user = LoginUser()
    user.username = flask.request.form.get('username', '')
    user.password = flask.request.form.get('password', '')
    db.session.add(user)
    db.session.commit()

    flask_login.login_user(user, remember=True)

    return flask.redirect(flask.url_for('index'))

def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    username = flask.request.form.get('username', '')
    password = flask.request.form.get('password', '')
    try:
        user = LoginUser.query.filter(LoginUser.username == username).one_or_none()
        if user == None:
            return flask.render_template('login.html', error='指定のユーザーは存在しません')
        elif user.password != password:
            return flask.render_template('login.html', error='パスワードが間違っています')
        else:
            flask_login.login_user(user, remember=True)
    except Exception as e:
        return flask.redirect(flask.url_for('index'))
    return flask.redirect(flask.url_for('index'))

@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('index'))
