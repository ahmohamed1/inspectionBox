from flask import Flask

UPLOAD_FOLDER = 'static/uploads/'

def create_app():
    app = Flask(__name__)
    app.secret_key = "secret key"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    from views1 import views

    app.register_blueprint(views, url_prefix='/')


    return app


app = create_app()
@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(debug=True)