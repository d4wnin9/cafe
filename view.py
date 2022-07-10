from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from database import db
from model import User, LoginUser, PermMenu, ABMenu
from util import o2s, s2o


def index():
    a_b_menu = ABMenu.query.filter(ABMenu.date == datetime.date.today()).first()
    perm_menu = db.session.query(PermMenu).all()
    return render_template('main.html', a_b_menu=a_b_menu, perm_menu=perm_menu, authed=current_user.is_authenticated)

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
    date_menu_price_calorie = s2o(user.date_menu_price_calorie)
    return render_template('history.html', user=user, date_menu_price_calorie=date_menu_price_calorie)


# DANGER ZONE

def add_menu():
    # TEST
    menu_list = [
        ABMenu(
            date='7-3',
            a_menu='焼き餃子の豆板醤ソースがけ',
            a_price=380,
            a_calorie=706,
            b_menu='豚肉の味噌炒め丼',
            b_price=320,
            b_calorie=675
        ),
        ABMenu(
            date='7-4',
            a_menu='和風おろしハンバーグ',
            a_price=380,
            a_calorie=697,
            b_menu='中華丼',
            b_price=320,
            b_calorie=599
        ),
        ABMenu(
            date='7-5',
            a_menu='牛肉の南蛮焼き',
            a_price=380,
            a_calorie=721,
            b_menu='チキン味噌カツ丼',
            b_price=320,
            b_calorie=764
        ),
        ABMenu(
            date='7-6',
            a_menu='白身魚の一口竜田揚げと串カツ',
            a_price=380,
            a_calorie=590,
            b_menu='照り焼きチキン丼',
            b_price=320,
            b_calorie=660
        ),
        PermMenu(menu='カレーライス', price='250', calorie='596'),
        PermMenu(menu='カツカレー', price='330', calorie='832'),
        PermMenu(menu='親子丼', price='280', calorie='698'),
        PermMenu(menu='カツ丼', price='280', calorie='944'),
        PermMenu(menu='カレーうどん', price='290', calorie='650'),
        PermMenu(menu='味噌ラーメン', price='210', calorie='530'),
        PermMenu(menu='醤油ラーメン', price='210', calorie='432'),
        PermMenu(menu='とんこつラーメン', price='210', calorie='476'),
        PermMenu(menu='かけうどん', price='160', calorie='325'),
        PermMenu(menu='かけそば', price='160', calorie='320'),
        PermMenu(menu='ライス(210g)', price='100', calorie='386')
    ]
    db.session.add_all(menu_list)
    db.session.commit()

    return redirect(url_for('index'))

def set_menu():
    db.session.query(PermMenu).delete()
    db.session.query(ABMenu).delete()
    db.session.commit()

    import json
    files = ['AB_6_27_30.json']
    a_b_menu_list = []
    perm_menu_list = []
    for file in files:
        with open(file, 'r') as f:
            menus = json.load(f)
        for menu in menus:
            date = list(menu.keys())[0]
            a_menu = menu[date]['Aセット']['name']
            a_price = menu[date]['Aセット']['price']
            a_calorie = menu[date]['Aセット']['calorie']
            b_menu = menu[date]['Bセット']['name']
            b_price = menu[date]['Bセット']['price']
            b_calorie = menu[date]['Bセット']['calorie']
            a_b_menu = ABMenu(
                date=date,
                a_menu=a_menu,
                a_price=a_price,
                a_calorie=a_calorie,
                b_menu=b_menu,
                b_price=b_price,
                b_calorie=b_calorie
            )
            a_b_menu_list.append(a_b_menu)
    db.session.add_all(a_b_menu_list)
    with open('permanent.json', 'r') as f:
        menus = json.load(f)
    for menu in menus:
        perm_menu = PermMenu(
            menu=menu['name'],
            price=menu['price'],
            calorie = menu['calorie']
        )
        perm_menu_list.append(perm_menu)
    db.session.add_all(perm_menu_list)
    db.session.commit()

    return redirect(url_for('index'))


def delete_menu():
    db.session.query(PermMenu).delete()
    db.session.query(ABMenu).delete()
    db.session.commit()

    return redirect(url_for('index'))

def delete_user():
    db.session.query(User).delete()
    db.session.commit()

    return redirect(url_for('index'))

def test_user():
    user = LoginUser.query.filter(LoginUser.username == 'ponyo').one_or_none()
    if user is None:
        user = LoginUser()
        user.username = 'ponyo'
        user.password = generate_password_hash('sosuke')
    db.session.add(user)
    db.session.commit()
    if user.date_menu_price_calorie == "":
        date_menu_price_calorie = []
    else:
        print(type(user.date_menu_price_calorie))
        date_menu_price_calorie = s2o(user.date_menu_price_calorie)
    date_menu_price_calorie.append(["2022/07/01", "カレー", 700, 1000])
    date_menu_price_calorie.append(["2022/07/02", "卵かけご飯", 400, 300])
    date_menu_price_calorie.append(["2022/07/03", "唐揚げ定食", 700, 1200])
    date_menu_price_calorie.append(["2022/07/04", "チョコレート", 200, 500])
    date_menu_price_calorie = o2s(date_menu_price_calorie)
    user.date_menu_price_calorie = date_menu_price_calorie
    user.calorie = 2000
    user.expense = 2000

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('login'))