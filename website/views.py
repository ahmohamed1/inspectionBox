from flask import request, redirect, render_template
from wtforms import SelectField
from flask_wtf import FlaskForm
# import flash to show the text message https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/
from flask import flash, Blueprint, url_for
import os
from werkzeug.utils import secure_filename
from .database_model import Project, Classes, db

# from .models import VGG as model

views = Blueprint('views', __name__)

UPLOAD_FOLDER = 'website/static/uploads/'
# This helper function use to check the extension of the file to make sure we load images
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'jfif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route('/')
def home_page():
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


class Form(FlaskForm):
    projects = SelectField('project', choices=[])
    classes = SelectField('classes', choices=[])


@views.route("/createproject", methods=['GET', 'POST'])
def create_project_page():
    if request.method == 'POST':
        project_name = request.form.get('name')
        description = request.form.get('description')
        classes = request.form.getlist('class[]')
        class_list = []
        # Check if there is project have same name
        project = Project.query.filter_by(name=project_name).first()
        if project:
            flash('project already exists.', category='error')
            return render_template('create_project.html')
        else:
            # Create project
            new_project = Project(name=project_name, description=description, nn_model="")
            db.session.add(new_project)
            db.session.commit()
            for class_name in classes:
                new_class = Classes(className=class_name, project_id=new_project.id, items_number=0)
                db.session.add(new_class)
                db.session.commit()
                class_list.append(class_name)
            flash('Project has been saved successfully', category='success')
            create_project_folder(new_project.name, class_list)
            return redirect(url_for('views.home_page'))
    return render_template('create_project.html')


def create_project_folder(project_name, classes):
    # make shots directory to save pics
    try:
        new_dir = os.path.join('./projects', project_name)
        os.mkdir(new_dir)
        print(new_dir)
        for cls in classes:
            class_dir = os.path.join(new_dir, 'dataset', 'train', cls)
            print(class_dir)
            os.makedirs(class_dir)
    except OSError as error:
        print(error)
