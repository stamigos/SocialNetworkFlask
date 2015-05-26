__author__ = 'amigos'
from flask import g
from profile import db, app
from datetime import datetime
import flask.ext.whooshalchemy as whooshalchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pytils

ROLE_STUDENT = 0
ROLE_TEACHER = 1


class User(db.Model):
    __tablename__ = "users"
    __searchable__ = ['last_name', 'first_name', 'father_name']
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column('last_name', db.String(20))
    first_name = db.Column('first_name', db.String(20))
    father_name = db.Column('father_name', db.String(20))
    password = db.Column('password', db.String(10))
    email = db.Column('email', db.String(50), unique=True, index=True)
    role = db.Column(db.SmallInteger, default=ROLE_STUDENT)
    registered_on = db.Column('registered_on', db.DateTime)
    posts = db.relationship('Post', backref='users', lazy='dynamic')

    def __init__(self, first_name, last_name, father_name, password, email, role):
        self.first_name = first_name
        self.last_name = last_name
        self.father_name = father_name
        self.password = password
        #self.set_password(password)
        self.email = email
        self.role = role
        self.registered_on = datetime.utcnow()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.last_name + self.first_name + self.father_name)


class Teacher(db.Model):
    __tablename__ = "teacher"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    unversities = db.relationship('University',
                                  backref=db.backref('teacher'))
    faculties = db.relationship('Faculty',
                                backref=db.backref('teacher'))
    subjects = db.relationship('Subject',
                               backref=db.backref('teacher'))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    university = db.Column('university', db.String(50))
    faculty = db.Column('faculty', db.String(50))


class Faculty(db.Model):
    id = db.Column('faculty_id', db.Integer, primary_key=True)
    name = db.Column('faculty_name', db.String(50))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))


class University(db.Model):
    id = db.Column('university_id', db.Integer, primary_key=True)
    name = db.Column('university_name', db.String(50))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))


class Subject(db.Model):

    id = db.Column('subject_id', db.Integer, primary_key=True)
    name = db.Column('subject_name', db.String(50))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, body):
        self.body = body
        self.timestamp = datetime.utcnow()
        self.user_id = g.user.id

    def __repr__(self):
        return '<Post %r>' % (
            self.body
        )


whooshalchemy.whoosh_index(app, User)