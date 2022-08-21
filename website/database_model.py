from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func  # this use to get  the data created


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(150), unique=True)
#     password = db.Column(db.String(150))
#     first_name = db.Column(db.String(150))
#     # Get the time and date we create the project
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     projects = db.relationship('Project')


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    description = db.Column(db.String(10000))
    #Classes = db.relationship('Classes')
    # Get the time and date we create the project
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    className = db.Column(db.String(120), unique=False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
