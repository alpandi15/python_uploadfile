import os
from app import app, services
from flask import Flask, flash, request, redirect, url_for, render_template
from flask import jsonify, make_response
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/oem/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_extension():
  return 'pdf'

@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
def index():
    return make_response(
      jsonify(
        info='Web Service Upload File for Printart',
        version='0.1'
      ), 200
    )

@app.route('/upload', methods = ['GET'])
def form_file():
  return render_template('upload.html')

@app.route('/upload', methods = ['POST'])
def upload_file():
  if request.method == 'POST':
    try:
      # check if the post request has the file part
      print("===========MASUK===========")
      if 'file' not in request.files:
        return make_response(jsonify(
            message='No selected file',
            succes=False
        ), 422)

      # process upload
      f = request.files['file']
      if f and allowed_file(f.filename):
        target = app.config['UPLOAD_FOLDER']
        if not services.check_directory(target):
          services.create_directory(target)
          return 'Tidak ada folder'
        return 'Ada folder'
        # filename = secure_filename(f.filename)
        # pathFile = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # # os.rename(pathFile, os.path.join(app.config['UPLOAD_FOLDER'], 'gantinama'))
        # f.save(pathFile)
        # return make_response(jsonify(
        #   message='file uploaded successfully',
        #   success=True,
        #   data=pathFile
        # ), 200)

      # if file not allowed
      return make_response(jsonify(
        message='File not supported',
        success=False
      ), 422)
    except ValueError:
      flash('No selected file')
      return make_response(jsonify(
        message='No selected file',
        success=False
      ), 422)