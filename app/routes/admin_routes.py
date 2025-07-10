from functools import wraps
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, verify_jwt_in_request, get_jwt
)
from app.models import db, User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def role_required(allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            role = claims.get("role")
            if role not in allowed_roles:
                return jsonify({"msg": "Forbidden: Admins only"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# Get all users (admin only)
@admin_bp.route("/users", methods=["GET"])
@role_required(['admin'])
def get_all_users():
    users = User.query.all()
    return jsonify([
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        } for user in users
    ]), 200

# Update a user's info (admin only)
@admin_bp.route("/users/<int:user_id>", methods=["PUT"])
@role_required(['admin'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json() or {}
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    user.role = data.get("role", user.role)

    db.session.commit()
    return jsonify({"msg": "User updated successfully"}), 200

# Delete a user (admin only)
@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
@role_required(['admin'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted successfully"}), 200
