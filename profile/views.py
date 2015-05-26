__author__ = 'amigos'
from flask import request, redirect, render_template, g, url_for, flash, Blueprint
from profile import db, app
from flask.ext.login import login_required, current_user
from flask.ext.login import LoginManager
from wtforms.ext.sqlalchemy.orm import model_form
from profile.forms import SearchForm, PostForm
from profile.resources import Resources
from profile.models import User, Post, ROLE_TEACHER, ROLE_STUDENT
import datetime

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

profile_page = Blueprint('profile', __name__, template_folder='templates')

resources = Resources(users=User, posts=Post)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    g.search_form = SearchForm()
    g.post_form = PostForm()


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    userisLecturer = False
    if g.user.role == ROLE_TEACHER:
        userisLecturer = True
    if g.user.role == ROLE_STUDENT:
        return render_template('profile.html')
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    posts = Post.query.filter_by(user_id=g.user.id)
    return render_template('dashboard.html', lecturer=g.user, posts=posts, userisLecturer=userisLecturer)


@app.route('/lecturer/<last_name>', methods=['GET', 'POST'])
@login_required
def lecturer(last_name):
    userisLecturer = False
    if g.user.role == ROLE_TEACHER:
        userisLecturer = True
    lecturer = User.query.filter_by(last_name=last_name).first()
    if lecturer is None:
        flash('Lecturer ' + last_name + ' not found.')
        return redirect(url_for('index'))
    posts = Post.query.filter_by(user_id=lecturer.id)
    return render_template('dashboard.html',
                           lecturer=lecturer,
                           posts=posts, userisLecturer=userisLecturer)


@app.route('/<curr_model>/', methods=['GET'])
@login_required
def get_list(curr_model):
    path = '/' + curr_model + '/'
    model = resources.get_context(str(curr_model))
    obj = db.session.query(model).all()
    return render_template('list_view.html',
                           obj=obj,
                           path=path)


@app.route('/<curr_model>/new/', methods=['GET'])
@login_required
def get_new(curr_model):
    path = '/' + curr_model + '/'
    model = resources.get_context(str(curr_model))
    Objform = model_form(model, db.session)
    form = Objform()
    action = path
    return render_template('detail_view.html',
                           action=action,
                           path=path,
                           form=form,
                           obj_id=model.id)


@app.route('/<curr_model>/<obj_id>/delete/', methods=['GET'])
@login_required
def get_delete(curr_model, obj_id):
    path = '/' + curr_model + '/'
    model = resources.get_context(str(curr_model))
    obj = db.session.query(model).get(obj_id)
    db.session.delete(obj)
    db.session.commit()
    return redirect(path)


@app.route('/<curr_model>/<obj_id>/edit/', methods=['GET'])
@login_required
def get_edit(curr_model, obj_id):
    path = '/' + curr_model + '/'
    model = resources.get_context(str(curr_model))
    ObjForm = model_form(model, db.session)
    obj = db.session.query(model).get(obj_id)
    form = ObjForm(obj=obj)
    return render_template('detail_view.html',
                           form=form,
                           action=path,
                           path=path,
                           obj_id=obj_id)


@app.route('/<curr_model>/', methods=['POST'])
@login_required
def post(curr_model, obj_id=''):
    model = resources.get_context(str(curr_model))
    if obj_id:
        obj = db.session.query(model).get(obj_id)
    else:
        obj = model()

    path = '/' + curr_model + '/'
    ObjForm = model_form(model, db.session)
    form = ObjForm(request.form)
    form.populate_obj(obj)

    db.session.add(obj)
    db.session.commit()

    return redirect(path)
