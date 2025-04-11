# app/auth.py

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from . import mongo

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    # Check if user already exists
    if mongo.db.users.find_one({'email': email}):
        return jsonify({'message': 'User already exists'}), 400

    # Store user with hashed password
    hashed_password = generate_password_hash(password)
    mongo.db.users.insert_one({'email': email, 'password': hashed_password})

    return jsonify({'message': 'User created successfully'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = mongo.db.users.find_one({'email': email})
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=email)
    return jsonify({'access_token': access_token}), 200
