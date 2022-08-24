from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func  # this use to get  the data created

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    description = db.Column(db.String(10000))
    nn_model = db.Column(db.String(150), unique=False)
    #Classes = db.relationship('Classes')
    # Get the time and date we create the project
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    className = db.Column(db.String(120), unique=False)
    items_number = db.Column(db.Integer, unique=False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))

    def to_dict(self):
        return {
            'className':self.className,
            'items_number': self.items_number
        }
