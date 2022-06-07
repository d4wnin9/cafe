from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

import config
import route


app = Flask(
    __name__,
    template_folder=config.TEMPLATE_FOLDER,
    static_folder=config.STATIC_FOLDER,
)
# user: team8
# pass: 1qazxsw2
# data: team8db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/team8db?user=team8&password=1qazxsw2'
app.config['SECRET_KEY'] = config.SECRET_KEY

route.add_route(app)
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from user import LoginUser
    return LoginUser.query.filter(LoginUser.id == user_id).one_or_none()

from database import db
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
