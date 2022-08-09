from flask import Flask, request, redirect, url_for, render_template
#import flash to show the text message https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/
from flask import flash, Blueprint
from flask import Markup
import urllib.request
import os
from werkzeug.utils import secure_filename
import model

views = Blueprint('views', __name__)

UPLOAD_FOLDER = 'static/uploads/'
# This helper function use to check the extension of the file to make sure we load images
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'jfif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/')
def home_page():
    return render_template("home.html")

@views.route("/prediction", methods=["GET","POST"])
def prediction_page():
    if 'file' not in request.files:
        flash('No file part')
        return render_template('prediction.html')
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return render_template('prediction.html')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        # Get the full path of the image and pass it into the model
        # to predict the image content
        img_path = os.path.join(UPLOAD_FOLDER, filename)
        flash('Image successfully uploaded and displayed below')
        classification, labels, values = model.predict_image(img_path)
        return render_template('prediction.html', filename=filename, prediction=classification, max=100, labels=labels, values=values)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@views.route("/datacollection")
def datacollection_page():
    return render_template("datacollection.html")

@views.route("/createproject", methods=['GET','POST'])
def create_project_page():
    if request.method == 'POST':
        project_name = request.form.get('name')
        fullname = request.form.getlist('class[]')
        print(project_name)
        for value in fullname:
            print(value)
    return render_template('create_project.html')

