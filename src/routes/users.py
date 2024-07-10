# src/routes/users.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User
from src import db

users_bp = Blueprint('users', __name__)

@users_bp.route('/users/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user:
        return jsonify({"msg": "User not found"}), 404

    if not current_user.is_admin:
        return jsonify({"msg": "Unauthorized"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()
    if "is_admin" in data:
        user.is_admin = data["is_admin"]
    db.session.commit()

    return jsonify(user.to_dict()), 200
