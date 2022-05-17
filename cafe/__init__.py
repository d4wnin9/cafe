from flask import Flask
import flask_login
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

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


if __name__ == '__main__':
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG_MODE,
        threaded=config.THREADED,
    )
