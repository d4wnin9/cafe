from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from database import db
from model import LoginUser
from util import d2s, s2d


def index():
    # authed
    if current_user.is_authenticated:
        return render_template("index.html")
    
    # unauthed
    return 'Login -> <a href="/login">/login</a>'

def register():
    # GET
    if request.method == 'GET':
        return render_template('register.html')

    # POST
    username = request.form.get('username')
    try:
        user = LoginUser.query.filter(LoginUser.username == username).one_or_none()
        if user == None:
            user = LoginUser()
            user.username = username
            user.password = generate_password_hash(request.form.get('password'))
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return redirect(url_for('index'))
        else:
            render_template('register.html', error='すでに使われている名前です')
    except Exception as e:
        return render_template('register.html', error=e)

def login():
    # GET
    if request.method == 'GET':
        return render_template('login.html')

    # POST
    username = request.form.get('username')
    try:
        user = LoginUser.query.filter(LoginUser.username == username).one_or_none()
        if user == None:
            return render_template('login.html', error='指定のユーザーは存在しません')
        elif not check_password_hash(user.password, request.form.get('password')):
            return render_template('login.html', error='パスワードが間違っています')
        else:
            login_user(user, remember=True)
            return redirect(url_for('index'))
    except Exception as e:
        return render_template('login.html', error=e)

@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_required
def history():
    username = current_user.username
    user = LoginUser.query.filter(LoginUser.username == username).one_or_none()

    # Test
    user.expense = 10101010
    user.calorie = 5000

    return render_template('history.html', user=user)
