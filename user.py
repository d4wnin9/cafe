from flask_login import UserMixin

from database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(255), unique=True)
    password = db.Column('password', db.String(255))

class LoginUser(UserMixin, User): 
    def get_id(self):
        return self.id
