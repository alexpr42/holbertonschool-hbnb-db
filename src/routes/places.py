from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.models.place import Place
from src.models.user import User
from src import db

places_bp = Blueprint('places', __name__)

@places_bp.route('/places', methods=['POST'])
@jwt_required()
def create_place():
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

    data = request.get_json()
    new_place = Place(**data)
    db.session.add(new_place)
    db.session.commit()
    return jsonify(new_place.to_dict()), 201

@places_bp.route('/places/<place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

    place = Place.query.get(place_id)
    if not place:
        return jsonify({"msg": "Place not found"}), 404

    data = request.get_json()
    for key, value in data.items():
        setattr(place, key, value)
    db.session.commit()
    return jsonify(place.to_dict()), 200

@places_bp.route('/places/<place_id>', methods=['DELETE'])
@jwt_required()
def delete_place(place_id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

    place = Place.query.get(place_id)
    if not place:
        return jsonify({"msg": "Place not found"}), 404

    db.session.delete(place)
    db.session.commit()
    return jsonify({"msg": "Place deleted"}), 200

