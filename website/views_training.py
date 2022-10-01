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
        self. project_name = session['project']
        project = Project.query.filter_by(name=self. project_name).first()
        clases_s = Classes.query.filter_by(project_id=project.id).all()
        self.model_save_directory = os.path.join('projects', self. project_name, 'models')
        self.project_id = project.id
        self.classes_path  = []
        self.model_name = None
        for cls in clases_s:
            path_ = os.path.join('projects', self. project_name, 'dataset', 'train', cls.className)
            self.classes_path.append(path_)

    def set_model_name(self, model_name):
        self.model_name = model_name

    def get_paths(self):
        return self.classes_path
    def get_class_number(self):
        return len(self.classes_path)

    def get_model_save_path(self):
        file_path = self.model_save_directory + '/ {}_{}.h5'.format(self. project_name,self.model_name)
        return file_path

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
    submit_save_model = SubmitField('Save Model')


@views_training.route('/train_page', methods=['GET', 'POST'])
def train_page():
    project_details = ProjectDetails()
    form = ModelForm(meta={'csrf': False})
    created_model = Create_model()
    if form.validate_on_submit():
        if form.submit_setup.data:
            created_model.setup(form.select_model.data,
                                form.optimizer.data,
                                form.learning_rate.data,
                                form.loss_function.data,
                                form.batch_size.data,
                                project_details.get_paths())
            created_model.build(project_details.get_class_number())
        if form.submit_start.data:
            created_model.train()
        if form.submit_stop.data:
            print("Stop")
        if form.submit_save_model.data:
            created_model.save_model(project_details.get_model_save_path())
            flash("The Model saved successfully at {}".format(project_details.get_model_save_path()))

    return render_template('train.html', form=form, show_modal=True)
