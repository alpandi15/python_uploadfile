from flask import Flask
import logging

app = Flask(__name__)
from app import controller

if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0')