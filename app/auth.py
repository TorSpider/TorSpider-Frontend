from flask_login import LoginManager

from app import app
from .models import User

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(id_):
    return User.query.get(int(id_))
