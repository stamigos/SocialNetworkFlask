__author__ = 'amigos'
from flask import request, redirect, url_for, render_template, g
from flask.ext.login import login_user, logout_user
from flask import Blueprint
from profile import db, app
from profile.views import profile_page
from profile.models import User
from werkzeug.security import check_password_hash

login_page = Blueprint('login', __name__, template_folder='templates')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_get'))


@app.route('/register', methods=['GET'])
def register_get():
        return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_post():
    user = User(first_name=request.form['first_name'], last_name=request.form['last_name'],
                father_name=request.form['father_name'], email=request.form['email'], password=request.form['password'],
                role=request.form['role'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('login_get'))


@app.route('/login', methods=['GET'])
def login_get():
        return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    registered_user = User.query.filter_by(email=email, password=password).first()
    if registered_user is None:
        return redirect(url_for('login_get'))
    login_user(registered_user)
    return redirect(request.args.get('next') or url_for('index'))