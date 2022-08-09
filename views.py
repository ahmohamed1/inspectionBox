from flask import Flask, request, redirect, url_for, render_template
#import flash to show the text message https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/
from flask import flash
from flask import Markup
import urllib.request
import os
from werkzeug.utils import secure_filename
import model

from server import app

# This helper function use to check the extension of the file to make sure we load images
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'jfif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home_page():
    return render_template("home.html")

@app.route("/prediction", methods=["GET","POST"])
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
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Get the full path of the image and pass it into the model
        # to predict the image content
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        flash('Image successfully uploaded and displayed below')
        classification, labels, values = model.predict_image(img_path)
        return render_template('prediction.html', filename=filename, prediction=classification, max=100, labels=labels, values=values)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route("/datacollection")
def datacollection_page():
    return render_template("datacollection.html")

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
