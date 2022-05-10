from flask import Flask
import flask_login
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from flask_wtf.csrf import CSRFProtect
import werkzeug.security as ws

from cafe import config
from cafe import route

# https://outputable.com/post/flask-login/
app = Flask(
    __name__,
    template_folder=config.TEMPLATE_FOLDER,
    static_folder=config.STATIC_FOLDER,
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cafe:cafe@database/cafe'
app.config['SECRET_KEY'] = config.SECRET_KEY

route.add_route(app)
csrf = CSRFProtect(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from cafe.user import LoginUser
    return LoginUser.query.filter(LoginUser.id == user_id).one_or_none()

from cafe.database import db
db.init_app(app)
with app.app_context():
    db.create_all()

'''
class LoginForm(flask_wtf.FlaskForm):
    username = wtforms.StringField(
        validators=[
            wtforms.validators.DataRequired()
        ]
    )

    password = wtforms.PasswordField(
        validators=[
            wtforms.validators.DataRequired()
        ]
    )

    submit = wtforms.SubmitField('Submit')

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise wtforms.validators.ValidationError('login error')
        if not ws.check_password_hash(user.password, self.password.data):
            raise wtforms.validators.ValidationError('login error')

    def get_user(self):
        return db.session.query(LoginUser).filter_by(username=self.username.data).first()


class RegistrationForm(flask_wtf.FlaskForm):
    username = wtforms.fields.StringField(
        validators=[
            wtforms.validators.DataRequired()
        ]
    )

    password = wtforms.PasswordField(
        validators=[
            wtforms.validators.DataRequired()
        ]
    )

    submit = wtforms.SubmitField('Submit')

    def validate_login(self, field):
        if db.session.query(LoginUser).filter_by(username=self.username.data).count() > 0:
            raise wtforms.validators.ValidationError('same username exists')
'''

if __name__ == '__main__':
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG_MODE,
        threaded=config.THREADED,
    )
