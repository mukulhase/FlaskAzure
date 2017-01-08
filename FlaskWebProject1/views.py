"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FlaskWebProject1 import app
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import visionconnect
import sys, traceback

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = visionconnect.getTag("http://lifegivesyoulemons.azurewebsites.net/" + url_for('static', filename='uploads/' + filename))
            try:
                trans = visionconnect.TranslateWord(data)
                #out = "<object>" + data + "</object>" + " " + "<translatedObj>" trans + "</translatedObj>"
                #return Response(out, mimetype='text/xml')
            except:
                trans = ''.join(traceback.format_stack())
            return "Uploaded " + data + " " + trans
    return render_template(
        'upload.html'
            )

@app.route('/uploadURL', methods=['GET', 'POST'])
def upload_URL():
    if request.method == 'POST':
        url = "http://www.yourmomhatesthis.com/images/2016/12/Fish-PNG-15.png"
        data = visionconnect.getTag(url)
        try:
            trans = visionconnect.TranslateWord(data)
            return "Uploaded " + data + " " +  trans
        except:
            trans = ''.join(traceback.format_stack())
        return "Uploaded " + data + " " + trans
    return render_template(
        'upload.html'
            )
