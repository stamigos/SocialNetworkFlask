__author__ = 'amigos'
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextField
from wtforms.validators import DataRequired, Required


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class PostForm(Form):
    post = StringField('post', validators=[DataRequired()])


class SearchForm(Form):
    search = StringField('search')