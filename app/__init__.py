from os import environ

from flask import Flask
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
app = Flask(__name__)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.jinja_env.add_extension('jinja2.ext.do')
app.threaded = True

config_path = environ.get("CONF_PATH", "app.config.ProductionConf")
app.config.from_object(config_path)
csrf.init_app(app)
db = SQLAlchemy(app)


# Views
@app.route('/test')
@login_required
def home():
    return 'Here you go!'


from app import models
from app import auth
from app.views import index, register, login, logout, nodes, invites, users
