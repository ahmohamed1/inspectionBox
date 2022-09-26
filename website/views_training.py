from flask import request, redirect, render_template, session
from wtforms import SelectField, StringField, IntegerField, FloatField, SubmitField, validators
from flask_wtf import FlaskForm
# import flash to show the text message https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/
from flask import flash, Blueprint, url_for
import os
import shutil
from werkzeug.utils import secure_filename
from .database_model import Project, Classes, db
from wtforms_sqlalchemy.fields import QuerySelectField


# from .models import VGG as model


views_training = Blueprint('views_training', __name__)


class ModelForm(FlaskForm):
    select_model = SelectField('select_model', choices=['ResNet10','ResNet18','ResNet50',
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
    submit_start = SubmitField('Start training')
    submit_stop = SubmitField('Stop training')


@views_training.route('/train_page', methods=['GET', 'POST'])
def train_page():
    form = ModelForm(meta={'csrf': False})

    if form.validate_on_submit():
        print(form.loss_function.data)
        print(form.optimizer.data)
        print(form.learning_rate.data)
        if form.submit_start.data:
            print("Start")
        if form.submit_stop.data:
            print("Stop")

    return render_template('train.html', form=form, show_modal=True)
