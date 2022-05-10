import flask_login
import wtforms

from cafe.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(255), unique=True)
    password = db.Column('password', db.String(255))

class LoginUser(flask_login.UserMixin, User): 
    def get_id(self):
        return self.id
