from flask import request, redirect, render_template, session
from wtforms import SelectField
from flask_wtf import FlaskForm
# import flash to show the text message https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/
from flask import flash, Blueprint, url_for
import os
from werkzeug.utils import secure_filename
from .database_model import Project, Classes, db
from wtforms_sqlalchemy.fields import QuerySelectField
# from .models import VGG as model

views = Blueprint('views', __name__)

UPLOAD_FOLDER = 'website/static/uploads/'
# This helper function use to check the extension of the file to make sure we load images
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'jfif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/')
def home_page():
    session['project'] = 'None'
    return render_template("home.html")

@views.route("/prediction", methods=["GET", "POST"])
def prediction_page():
    if 'file' not in request.files:
        flash('No file part', category='error')
        return render_template('prediction.html')
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading', category='error')
        return render_template('prediction.html')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        # Get the full path of the image and pass it into the model
        # to predict the image content
        img_path = os.path.join(UPLOAD_FOLDER, filename)
        flash('Image successfully uploaded and displayed below', category='success')
        # classification, labels, values = model.predict_image(img_path)
        classification = 'none'
        return render_template('prediction.html', filename=filename, prediction=classification, max=100)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif', category='error')
        return redirect(request.url)

