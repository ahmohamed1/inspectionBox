from flask import request, redirect, render_template
from flask import session, send_from_directory, url_for, Response
from wtforms import SelectField, FileField, SubmitField
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
import cv2

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


class LoadImage(FlaskForm):
    image = FileField('image', validators=[FileRequired()])
    submit = SubmitField('Predict')


def generate_frames(filename):
    ## read the camera frame
    print(filename)
    frame = cv2.imread(filename)
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

@views.route('/display/<filename>')
def imshow(filename):
    print(filename)
    return Response(generate_frames(filename), mimetype='multipart/x-mixed-replace; boundary=frame')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/')
def home_page():
    session['project'] = 'None'
    return render_template("home.html")

@views.route("/prediction", methods=["GET", "POST"])
def prediction_page():
    form = LoadImage()
    file_url = None
    if form.validate_on_submit():
        file = form.image.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            # Get the full path of the image and pass it into the model
            # to predict the image content
            img_path = os.path.join(UPLOAD_FOLDER, filename)
            print(img_path)
            flash('Image successfully uploaded and displayed below', category='success')
            # classification, labels, values = model.predict_image(img_path)
            classification = 'none'
            file_url = img_path
            #return render_template('prediction.html', filename=img_path, prediction=classification, max=100, form=form)
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif', category='error')
            #return redirect(request.url)
    return render_template('prediction.html', form=form, file_url=file_url)

