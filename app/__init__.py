from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from mongoengine import connect
from flask_jwt_extended import JWTManager
from .models import User 

import os

load_dotenv()

app = Flask(__name__)
CORS(app) # I need to change this to only allow the frontend to access
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

database_uri = os.environ.get("DATABASE_URL")
connect(host=database_uri)

jwt = JWTManager(app)

from . import routes