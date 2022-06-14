from flask_login import UserMixin

from database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(255), unique=True, nullable=False)
    password = db.Column('password', db.String(255), nullable=False)
    date_menu = db.Column('date_menu', db.String(2**12 - 1), nullable=False, default="")
    expense = db.Column('expense', db.Integer, nullable=False, default=0)
    calorie = db.Column('calorie', db.Integer, nullable=False, default=0)

class LoginUser(UserMixin, User): 
    def get_id(self):
        return self.id
