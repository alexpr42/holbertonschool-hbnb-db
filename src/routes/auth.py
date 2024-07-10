# src/routes/auth.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from src.models.user import User
from src import bcrypt, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=str(user.id), additional_claims={"is_admin": user.is_admin})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid credentials"}), 401
