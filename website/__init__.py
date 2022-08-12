from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

UPLOAD_FOLDER = 'website/static/uploads/'

def create_app():
    app = Flask(__name__)
    app.secret_key = "secret key"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    # Define the database with flask
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    from .database_model import Project, Classes
    create_database(app)

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

app = create_app()
