from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from mongoengine import connect
from flask_jwt_extended import JWTManager
import os

load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}) # change this in production

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

database_uri = os.environ.get("DATABASE_URL")
connect(host=database_uri)

jwt = JWTManager(app)

from .routes import api_bp 
app.register_blueprint(api_bp)
