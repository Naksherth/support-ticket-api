from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.models import db, User
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.schemas.register_schema import RegisterSchema

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
register_schema = RegisterSchema()

@auth_bp.route('/register', methods=['POST'])
def register():
    json_data = request.get_json() or {}

    # Validate input using schema
    errors = register_schema.validate(json_data)
    if errors:
        return jsonify(errors), 400

    try:
        data = register_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    username = data['username']
    email = data['email']
    password = data['password']
    role = data['role'].lower()

    # Check if user exists
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"msg": "User already exists"}), 409

    # Create and save user
    user = User(username=username, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    json_data = request.get_json() or {}

    username = json_data.get('username')
    password = json_data.get('password')

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )
    return jsonify(access_token=access_token), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)   # Convert the identity to int if stored as string
    except ValueError:
        return jsonify({"msg": "Invalid user id in token"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    })
