from flask_login import UserMixin

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

    menu = db.Column('menu', db.String(32), nullable=False)
    price = db.Column('price', db.Integer, nullable=False)
    calorie = db.Column('calorie', db.Integer, nullable=False)


class ABMenu(db.Model):
    __tablename__ = 'a_b_menu'

    date = db.Column('date', db.String(8), nullable=False)
    a_menu = db.Column('menu', db.String(32), nullable=False)
    a_price = db.Column('price', db.Integer, nullable=False)
    a_calorie = db.Column('calorie', db.Integer, nullable=False)
    b_menu = db.Column('menu', db.String(32), nullable=False)
    b_price = db.Column('price', db.Integer, nullable=False)
    b_calorie = db.Column('calorie', db.Integer, nullable=False)
