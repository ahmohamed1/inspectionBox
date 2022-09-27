from flask import request, redirect, render_template, session
from wtforms import SelectField, StringField, IntegerField, FloatField, SubmitField, validators
from flask_wtf import FlaskForm
# import flash to show the text message https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/
from flask import flash, Blueprint, url_for
import os
import shutil
from werkzeug.utils import secure_filename
from .database_model import Project, Classes, db
from .dl_model import Create_model
from wtforms_sqlalchemy.fields import QuerySelectField


# from .models import VGG as model


views_training = Blueprint('views_training', __name__)

class ProjectDetails():
    def __init__(self):
        project_name = session['project']
        project = Project.query.filter_by(name=project_name).first()
        clases_s = Classes.query.filter_by(project_id=project.id).all()
        self.project_id = project.id
        self.classes_path  = []
        for cls in clases_s:
            path_ = os.path.join('projects', project_name, 'dataset', 'train', cls.className)
            self.classes_path.append(path_)

    def get_paths(self):
        for path in self.classes_path:
            print(path)

    def get_class_number(self):
        return len(self.classes_path)
class ModelForm(FlaskForm):
    select_model = SelectField('select_model', choices=['ResNet50','ResNet101','ResNet152',
                                                        'VGG16','VGG19'])
    batch_size = SelectField('batch_size', choices=['8','16','32'])
    learning_rate = FloatField('learning_rate', validators=[validators.InputRequired()])
    optimizer = SelectField('optimizer', choices=['Adadelta', 'Adagrad', 'Adam', 'RMSprop', 'SGD'])
    loss_function = SelectField('loss_function', choices=['mean_squared_error',
                                                          'mean_absolute_error',
                                                          'binary_crossentropy',
                                                          'categorical_crossentropy',
                                                          'sparse_categorical_crossentropy',
                                                          'kullback_leibler_divergence'])
    submit_setup = SubmitField('Setup the model')
    submit_start = SubmitField('Start training')
    submit_stop = SubmitField('Stop training')


@views_training.route('/train_page', methods=['GET', 'POST'])
def train_page():
    project_details = ProjectDetails()
    form = ModelForm(meta={'csrf': False})
    if form.validate_on_submit():
        if form.submit_setup.data:
            created_mode = Create_model(form.select_model.data,
                                        form.optimizer.data,
                                        form.learning_rate.data,
                                        form.loss_function.data,
                                        form.batch_size.data)
            created_mode.build(project_details.get_class_number())
        if form.submit_start.data:
            print("Start")
        if form.submit_stop.data:
            print("Stop")

    return render_template('train.html', form=form, show_modal=True)
