import os
from app import app, services
from flask import Flask, flash, request, render_template
from flask import jsonify, make_response
from werkzeug.utils import secure_filename

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
      if 'file' not in request.files:
        return make_response(jsonify(
            message='No selected file',
            succes=False
        ), 422)

      # process upload
      file = request.files['file']
      if file and services.allowed_file(file.filename):
        target = app.config['UPLOAD_FOLDER']
        # check available path upload
        if not services.check_directory(target):
          services.create_directory(target)
        
        # upload fle
        resUpload = services.upload(file)
        if resUpload:
          return make_response(jsonify(
            message='file uploaded successfully',
            success=True,
            data=resUpload
          ), 200)
        return make_response(jsonify(
            message='Upload Error',
            success=False
          ), 422)

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