import datetime, time
import os

import cv2
from flask import flash, Blueprint, Response, redirect
from flask import request, render_template, jsonify

from .database_model import Project, Classes

global project_name, class_name
global camera_switch, save_image
camera_switch = False
save_image = False
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
        return jsonify(random_text="OK")
    return jsonify(random_text="OK")


def generate_frames():
    global save_image, project_name, class_name
    while True:
        ## read the camera frame
        success, frame = camera.read()
        if success:
            if save_image:
                save_image = 0
                now = datetime.datetime.now()
                path_ = os.path.join('projects', project_name, 'dataset', 'train', class_name)
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


def get_dropdown_values():
    """
    dummy function, replace with e.g. database call. If data not change, this function is not needed but dictionary
could be defined globally
    """

    # Create a dictionary (myDict) where the key is
    # the name of the brand, and the list includes the names of the car models
    #
    # Read from the database the list of cars and the list of models.
    # With this information, build a dictionary that includes the list of models by brand.
    # This dictionary is used to feed the drop down boxes of car brands and car models that belong to a car brand.
    #
    # Example:
    #
    # {'Toyota': ['Tercel', 'Prius'],
    #  'Honda': ['Accord', 'Brio']}

    projects = Project.query.all()
    # Create an empty dictionary
    myDict = {}
    for p in projects:

        key = p.name
        project_id = p.id

        # Select all car models that belong to a car brand
        q = Classes.query.filter_by(project_id=project_id).all()

        # build the structure (lst_c) that includes the names of the car models that belong to the car brand
        lst_c = []
        for c in q:
            lst_c.append(c.className)
        myDict[key] = lst_c
    class_entry_relations = myDict
    return class_entry_relations


@collectData.route('/_update_dropdown')
def update_dropdown():
    # the value of the first dropdown (selected by the user)
    selected_class = request.args.get('selected_class', type=str)

    # get values for the second dropdown
    updated_values = get_dropdown_values()[selected_class]

    # create the value sin the dropdown as a html string
    html_string_selected = ''
    for entry in updated_values:
        html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)

    return jsonify(html_string_selected=html_string_selected)


@collectData.route('/_process_data')
def process_data():
    global project_name, class_name
    selected_class = request.args.get('selected_class', type=str)
    selected_entry = request.args.get('selected_entry', type=str)
    project_name = selected_class
    class_name = selected_entry
    # process the two selected values here and return the response; here we just create a dummy string
    return jsonify(random_text="You selected Project: {} and class: {}.".format(selected_class, selected_entry))


@collectData.route('/datacollection', methods=['POST', 'GET'])
def index():
    global project_name
    #initialize drop down menus
    class_entry_relations = get_dropdown_values()
    default_classes = sorted(class_entry_relations.keys())
    default_values = class_entry_relations[default_classes[0]]

    #class_list = {'data':[cls.to_dict() for cls in Classes.query.filter_by(name=project_name).all()]}
    return render_template('datacollection.html',
                           all_classes=default_classes,
                           allDatas_entries=default_values)
