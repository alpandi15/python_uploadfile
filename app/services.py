import os
from app import app
from flask import request
from flask import jsonify, make_response
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/oem/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def check_directory(dir):
  if os.path.isdir(dir): return True
  return False

def create_directory(dir):
  if not check_directory(dir):
    res = os.mkdir(dir)
    return res

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_extension():
  return 'pdf'

def upload(file):
  target = app.config['UPLOAD_FOLDER']
  filename = secure_filename(file.filename)
  pathFile = os.path.join(target, filename)
  upload = file.save(pathFile)
  return pathFile