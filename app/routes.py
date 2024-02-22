from flask import request, jsonify
from flask_jwt_extended import create_access_token
from . import app, jwt  
from .models import User

@app.route('/')
def hello_world():
    return 'Hello, Aeroblocks!'

@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    
    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    if User.objects(email=email).first():
        return jsonify({"msg": "Email already used"}), 409

    user = User(email=email)
    user.set_password(password)
    user.save()

    return jsonify({"msg": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    
    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    user = User.objects(email=email).first()
    
    if user is None or not user.check_password(password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200
