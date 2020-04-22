from app import app
import os

def check_directory(dir):
  if os.path.isdir(dir): return True
  return False

def create_directory(dir):
  if not check_directory(dir):
    res = os.mkdir(dir)
    return res