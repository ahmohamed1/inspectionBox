import datetime, time
import os

import cv2
from flask import flash, Blueprint, Response, redirect, session
from flask import request, render_template, jsonify, url_for

from .database_model import Project, Classes

from flask_wtf import FlaskForm, Form
from wtforms import StringField, validators, IntegerField, FloatField, SelectField
from wtforms_sqlalchemy.fields import QuerySelectField


global class_name, project_name, class_id
global camera_switch, save_image
camera_switch = 1
save_image = 0
camera = cv2.VideoCapture(0)
collectData = Blueprint('collectData', __name__)

train_page = Blueprint('train_page', __name__)

class TrainingParameter(FlaskForm):
    select_model = StringField('select_model')
    batch_size = IntegerField('batch_size')
    learning_rate = FloatField('learning_rate')
    optimizer = SelectField('optimizer', choices=['Adadelta', 'Adagrad', 'Adam', 'RMSprop', 'SGD'])
    loss_function = SelectField('loss_function', choices=['mean_squared_error', 'mean_absolute_error',
                                                          'binary_crossentropy', 'categorical_crossentropy',
                                                          'sparse_categorical_crossentropy', 'kullback_leibler_divergence'])