from flask import request, redirect, render_template, session
from wtforms import SelectField, StringField, IntegerField
from flask_wtf import FlaskForm, Form
# import flash to show the text message https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/
from flask import flash, Blueprint, url_for
import os
import shutil
from werkzeug.utils import secure_filename
from .database_model import Project, Classes, db
from wtforms_sqlalchemy.fields import QuerySelectField
# from .models import VGG as model



views_projects = Blueprint('views_projects', __name__)


def choice_query():
    return Project.query

def add_classes(classes, project_name, project_id):
    class_list = []
    for class_name in classes:
        new_class = Classes(className=class_name, project_id=project_id, items_number=0)
        db.session.add(new_class)
        db.session.commit()
        class_list.append(class_name)
    create_project_folder(project_name, class_list)

class ChoiceForm(FlaskForm):
    opts = QuerySelectField(query_factory=choice_query, allow_blank=True)

class ProjectForm(FlaskForm):
    class_id = IntegerField('ID')
    class_name = StringField('name')
    class_number = IntegerField('number of items')


@views_projects.route('/select_project', methods=['GET', 'POST'])
def select_project():
    form = ChoiceForm()
    if form.validate_on_submit():
        flash('Project {} has been selected!!!'.format(form.opts.data), category='success')
        session["project"] = str(form.opts.data)
    return render_template('selectproject.html', form=form)


@views_projects.route('/project_info', methods=['GET', 'POST'])
def project_info():
    project_name = session['project']
    project = Project.query.filter_by(name=project_name).first()
    classes = Classes.query.filter_by(project_id=project.id).all()
    table_form = ProjectForm()
    add_class_form = ProjectForm()
    delete_class_form = ProjectForm()

    if add_class_form.validate_on_submit():
        cls = add_class_form.class_name.data
        add_classes([cls], project.name, project.id)
        flash("Class {} added succesfully!!".format(cls), category='success')
        return redirect(url_for('views_projects.project_info'))
    return render_template('project_info.html',
                           form=add_class_form,
                           delete_class_form=delete_class_form,
                           classes=classes)

@views_projects.route("/project_info/<int:class_id>", methods=['GET', 'POST'])
def delect_class(class_id):
    if request.method == "POST":
        cls = Classes.query.get_or_404(class_id)
        db.session.delete(cls)
        db.session.commit()
        delete_class_folder(session['project'], cls.className)
        flash("Class {} has been deleted successfully!!!".format(cls.className), category="success")
        return redirect(url_for('views_projects.project_info'))
    return redirect(url_for('views_projects.project_info'))

@views_projects.route("/createproject", methods=['GET', 'POST'])
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
            add_classes(classes, new_project.name, new_project.id)
            flash('Project has been saved successfully', category='success')
            return redirect(url_for('views.home_page'))
    return render_template('create_project.html')

def create_project_folder(project_name, classes):
    # make shots directory to save pics
    try:
        new_dir = os.path.join('projects', project_name)
        if os.path.isfile(new_dir):
            print(new_dir)
            os.mkdir(new_dir)
        for cls in classes:
            class_dir = os.path.join(new_dir, 'dataset', 'train', cls)
            os.makedirs(class_dir)
            print(class_dir)
    except OSError as error:
        print(error)

def delete_class_folder(project_name, cls):
    # make shots directory to save pics
    try:
        new_dir = os.path.join('projects', project_name)
        class_dir = os.path.join(new_dir, 'dataset', 'train', cls)
        if os.path.exists(class_dir) and os.path.isdir(class_dir):
            shutil.rmtree(class_dir)
    except OSError as error:
        print(error)