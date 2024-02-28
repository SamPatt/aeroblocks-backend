from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from . import app, jwt  
from .models import User, CanvasState
import mongoengine.errors
from datetime import timedelta, datetime
from .lex import lex_code

api_bp = Blueprint('api', __name__, url_prefix='/api')

@app.route('/')
def hello_world():
    return 'Hello, Aeroblocks!'

@api_bp.route('/register', methods=['POST'])
def register():
    try:
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
    except mongoengine.errors.ValidationError as e:
        return jsonify({"msg": "Invalid data format", "errors": str(e)}), 422
    except Exception as e:
        return jsonify({"msg": "Registration failed", "errors": str(e)}), 500

@api_bp.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        
        if not email or not password:
            return jsonify({"msg": "Missing email or password"}), 400

        user = User.objects(email=email).first()
        
        if user is None or not user.check_password(password):
            return jsonify({"msg": "Invalid email or password"}), 401

        expires_delta = timedelta(hours=3)
        access_token = create_access_token(identity=email, expires_delta=expires_delta)
        return jsonify(access_token=access_token), 200
    except Exception as e:
        return jsonify({"msg": "Login failed", "errors": str(e)}), 500

@api_bp.route('/canvas/create', methods=['POST'])
@jwt_required()
def create_canvas():
    current_user_email = get_jwt_identity()
    user = User.objects(email=current_user_email).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    name = data.get('name')
    code = data.get('code')
    
    initial_canvas_state = lex_code(code)

    new_canvas = CanvasState(name=name, data=initial_canvas_state)
    user.canvases.append(new_canvas)
    user.save()


    canvas_dict = {
        "name": new_canvas.name,
        "data": new_canvas.data,
        "created_at": new_canvas.created_at.isoformat(),
        "updated_at": new_canvas.updated_at.isoformat()
    }

    return jsonify({"message": "Canvas created successfully", "canvas": canvas_dict}), 201

@api_bp.route('/canvas/load', methods=['GET'])
@jwt_required()
def load_canvases():
    current_user_email = get_jwt_identity()
    user = User.objects(email=current_user_email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    canvases = [{
        "name": canvas.name,
        "data": canvas.data,
        "created_at": canvas.created_at.isoformat(),
        "updated_at": canvas.updated_at.isoformat()
    } for canvas in user.canvases]

    return jsonify(canvases), 200

@api_bp.route('/canvas/save', methods=['POST'])
@jwt_required()
def save_canvas():
    current_user_email = get_jwt_identity()
    user = User.objects(email=current_user_email).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    canvas_name = data.get('name')
    new_data = data.get('data')

    canvas_found = False
    for canvas in user.canvases:
        if canvas.name == canvas_name:
            canvas.data = new_data
            canvas.updated_at = datetime.now()
            canvas_found = True
            break

    if not canvas_found:
        new_canvas = CanvasState(name=canvas_name, data=new_data, updated_at=datetime.now())
        user.canvases.append(new_canvas)

    user.save()
    return jsonify({"message": "Canvas saved successfully"}), 200
