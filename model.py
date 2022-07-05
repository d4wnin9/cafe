from flask_login import UserMixin
import datetime

from database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(255), unique=True, nullable=False)
    password = db.Column('password', db.String(255), nullable=False)
    date_menu = db.Column('date_menu', db.String(2**12), nullable=False, default="")
    expense = db.Column('expense', db.Integer, nullable=False, default=0)
    calorie = db.Column('calorie', db.Integer, nullable=False, default=0)

class LoginUser(UserMixin, User): 
    def get_id(self):
        return self.id


class PermMenu(db.Model):
    __tablename__ = 'permanent_menu'

    id = db.Column('id', db.Integer, primary_key=True)
    menu = db.Column('menu', db.String(32), nullable=False)
    price = db.Column('price', db.Integer, nullable=False)
    calorie = db.Column('calorie', db.Integer, nullable=False)
    out_of_stock = db.Column('out_of_stock', db.Boolean, nullable=False, default=False)

    def __init__(self, menu, price, calorie):
        self.menu = menu
        self. price = price
        self.calorie = calorie


class ABMenu(db.Model):
    __tablename__ = 'a_b_menu'

    id = db.Column('id', db.Integer, primary_key=True)
    date = db.Column('date', db.Date, nullable=False)
    a_menu = db.Column('a_menu', db.String(32), nullable=False)
    a_price = db.Column('a_price', db.Integer, nullable=False)
    a_calorie = db.Column('a_calorie', db.Integer, nullable=False)
    a_out_of_stock = db.Column('a_out_of_stock', db.Boolean, nullable=False, default=False)
    b_menu = db.Column('b_menu', db.String(32), nullable=False)
    b_price = db.Column('b_price', db.Integer, nullable=False)
    b_calorie = db.Column('b_calorie', db.Integer, nullable=False)
    b_out_of_stock = db.Column('b_out_of_stock', db.Boolean, nullable=False, default=False)

    def __init__(self, date, a_menu, a_price, a_calorie, b_menu, b_price, b_calorie):
        self.date = datetime.date(2022, *map(int, date.split('-')))
        self.a_menu = a_menu
        self.a_price = a_price
        self.a_calorie = a_calorie
        self.b_menu = b_menu
        self.b_price = b_price
        self.b_calorie = b_calorie

