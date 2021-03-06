from os import environ

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.contrib.fixers import ProxyFix
import requests_cache

csrf = CSRFProtect()
app = Flask(__name__)
# Using requests_cache we can avoid constantly having to make API calls to the backend for simple web data.
requests_cache.install_cache('api_cache', backend='memory', expire_after=480)


app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.jinja_env.add_extension('jinja2.ext.do')
app.threaded = True

app.wsgi_app = ProxyFix(app.wsgi_app)

config_path = environ.get("CONF_PATH", "app.config.ProductionConf")
app.config.from_object(config_path)
csrf.init_app(app)
db = SQLAlchemy(app)

from app import models
from app import auth
from app.views import index, register, login, logout, nodes, invites, users, top20
