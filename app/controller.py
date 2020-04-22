import os
import logging
from app import app
from flask import Flask, flash, request, redirect, url_for, render_template
from flask import jsonify, make_response
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)
UPLOAD_FOLDER = '/home/oem/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
def index():
    return make_response(jsonify(
      info='Web Service Upload File for Printart',
      version='0.1'
    ), 200
    )

@app.route('/upload')
def form_file():
  return render_template('upload.html')

def allowed_file(filename):
  return '.' in filename and \
      filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    try:
      # check if the post request has the file part
      logging.info("================MASUK==================")
      if 'file' not in request.files:
        return make_response(jsonify(
            message='No selected file',
            succes=False
        ), 422)
      f = request.files['file']
      if f and allowed_file(f.filename):
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return make_response(jsonify(
          message='file uploaded successfully',
          success=True
        ), 200)
      return make_response(jsonify(
        message='File not supported',
        success=False
      ), 200)
    except ValueError:
      flash('No selected file')
      return make_response(jsonify(
        message='No selected file',
        success=False
      ), 422)