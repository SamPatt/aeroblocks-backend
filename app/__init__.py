from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from mongoengine import connect
from flask_jwt_extended import JWTManager
import os

load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "https://aeroblocks.tech"}}, supports_credentials=True, allow_headers=["Content-Type", "Authorization"])

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
jwt = JWTManager(app)

database_uri = os.environ.get("DATABASE_URL")
connect(host=database_uri)


from .routes import api_bp 
app.register_blueprint(api_bp)
