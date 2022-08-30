import datetime, time
import os

import cv2
from flask import flash, Blueprint, Response, redirect, session
from flask import request, render_template, jsonify

from .database_model import Project, Classes

from flask_wtf import FlaskForm, Form
from wtforms_sqlalchemy.fields import QuerySelectField


global class_name
global camera_switch, save_image
camera_switch = 1
save_image = 0
camera = cv2.VideoCapture(0)
collectData = Blueprint('collectData', __name__)


# https://towardsdatascience.com/camera-app-with-flask-and-opencv-bd147f6c0eec
@collectData.route('/requests', methods=['POST', 'GET'])
def tasks():
    global camera_switch, camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global save_image
            save_image = 1
        elif request.form.get('stop') == 'Stop/Start':
            if camera_switch == 1:
                camera_switch = 0
                camera.release()
                cv2.destroyAllWindows()
            else:
                camera = cv2.VideoCapture(0)
                camera_switch = 1

    elif request.method == 'GET':
        return redirect(url_for('collectData.index'))
    return redirect(url_for('collectData.index'))

def generate_frames():
    global save_image, class_name
    while True:
        ## read the camera frame
        success, frame = camera.read()
        if success:
            if save_image:
                save_image = 0
                flash("Save", category="success")
                now = datetime.datetime.now()
                path_ = os.path.join('projects', session['project'], 'dataset', 'train', class_name)
                p = os.path.sep.join([path_, "shot_{}.png".format(str(now).replace(":", ''))])
                cv2.imwrite(p, frame)
                cls = Classes.query.filter_by(class_name=class_name).first()
                setattr(cls, 'no_of_logins', cls.items_number + 1)
                print(p)
            try:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                flash("No image was captured", category='error')
                pass
        else:
            pass

@collectData.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def choice_query():
    project_name = session['project']
    project = Project.query.filter_by(name=project_name).first()
    classes = Classes.query.filter_by(project_id=project.id).all()
    return classes

class ChoiceForm(FlaskForm):
    opts = QuerySelectField(query_factory=choice_query, allow_blank=True)

@collectData.route('/datacollection', methods=['POST', 'GET'])
def index():
    global class_name
    form = ChoiceForm()
    project_name = session['project']
    project = Project.query.filter_by(name=project_name).first()
    classes = Classes.query.filter_by(project_id=project.id).all()
    if form.validate_on_submit():
        class_name = str(form.opts.data)
        flash("Class {} selected!!".format(class_name), category='success')
    #class_list = {'data':[cls.to_dict() for cls in Classes.query.filter_by(name=project_name).all()]}
    return render_template('datacollection.html',
                           classes=classes,
                           form=form)
