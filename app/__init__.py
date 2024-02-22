from flask import Flask
from dotenv import load_dotenv
from flask_pymongo import PyMongo
import os

load_dotenv()

app = Flask(__name__)

app.config['MONGO_URI'] = os.environ.get('DATABASE_URL')

mongo = PyMongo(app)


@app.route('/')
def hello_world():
    return 'Hello, Aeroblocks!'

@app.route('/test_db')
def test_db():
    try:
        return 'Connected to the database successfully!'
    except Exception as e:
        return 'Failed to connect to the database: ' + str(e)
