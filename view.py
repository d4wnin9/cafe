from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from database import db
from model import User, LoginUser, PermMenu, ABMenu
from util import d2s, s2d


def index():
    # authed
    if current_user.is_authenticated:

        # TEST
        menu_list = [
            ABMenu(
                date='6-21',
                a_menu='焼き餃子の豆板醤ソースがけ',
                a_price=380,
                a_calorie=706,
                b_menu='豚肉の味噌炒め丼',
                b_price=320,
                b_calorie=675
            ),
            ABMenu(
                date='6-28',
                a_menu='和風おろしハンバーグ',
                a_price=380,
                a_calorie=697,
                b_menu='中華丼',
                b_price=320,
                b_calorie=599
            ),
            ABMenu(
                date='6-29',
                a_menu='牛肉の南蛮焼き',
                a_price=380,
                a_calorie=721,
                b_menu='チキン味噌カツ丼',
                b_price=320,
                b_calorie=764
            ),
            ABMenu(
                date='6-30',
                a_menu='白身魚の一口竜田揚げと串カツ',
                a_price=380,
                a_calorie=590,
                b_menu='照り焼きチキン丼',
                b_price=320,
                b_calorie=660
            )
        ]
        db.session.add_all(menu_list)
        db.session.commit()

        a_b_menu = ABMenu.query.filter(ABMenu.date == datetime.date.today()).first()
        return render_template("index.html", a_b_menu=a_b_menu)
    
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

    return render_template('history.html', user=user)


# DANGER ZONE
def delete_menu():
    db.session.query(PermMenu).delete()
    db.session.query(ABMenu).delete()
    db.session.commit()

    return render_template('index.html')

def delete_user():
    db.session.query(User).delete()
    db.session.commit()

    return render_template('index.html')
