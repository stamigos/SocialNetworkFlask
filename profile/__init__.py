__author__ = 'amigos'
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')
app.config.from_object('config')
db = SQLAlchemy(app)

from profile import models, views
from reg_auth.views import login_page
from profile.views import profile_page
from search.views import search_page

app.register_blueprint(login_page)
app.register_blueprint(search_page)
app.register_blueprint(profile_page)