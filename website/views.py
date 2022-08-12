from flask import request, redirect, render_template
#import flash to show the text message https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/
from flask import flash, Blueprint, url_for
import os
from werkzeug.utils import secure_filename
from .database_model import Project, Classes, db

from .models.VGG import model

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
        classification, labels, values = model.predict_image(img_path)
        return render_template('prediction.html', filename=filename, prediction=classification, max=100, labels=labels, values=values)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif',category='error')
        return redirect(request.url)

@views.route("/datacollection")
def datacollection_page():
    return render_template("datacollection.html")

@views.route("/createproject", methods=['GET','POST'])
def create_project_page():
    if request.method == 'POST':
        project_name = request.form.get('name')
        description = request.form.get('description')
        classes = request.form.getlist('class[]')

        # Check if there is project have same name
        project = Project.query.filter_by(name=project_name).first()
        if project:
            flash('project already exists.', category='error')
            return render_template('create_project.html')
        else:
            # Create project
            new_project = Project(name=project_name, description=description)
            db.session.add(new_project)
            db.session.commit()
            flash('Project has been saved successfully', category='success')
            return redirect(url_for('views.home_page'))
    return render_template('create_project.html')

# capture = cv2.VideoCapture(0)
#
# def load_video(cap):
#     while(True):
#         sucssess, image = cap.read()
#         if not sucssess:
#             print("could not load video")
#             break;
#
#         yield image

# @views.route('/video')
# def display_video():
#     global capture
#
#     # Return the result on the web
#     return Response(load_video(capture),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')