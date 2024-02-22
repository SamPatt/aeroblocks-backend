from flask import Flask
from dotenv import load_dotenv
from mongoengine import connect
from flask_jwt_extended import JWTManager
from .models import User 

import os

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

database_uri = os.environ.get("DATABASE_URL")
connect(host=database_uri)

jwt = JWTManager(app)

from . import routes