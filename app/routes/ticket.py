from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
from app.models import db, Ticket, AuditLog
from app.schemas.ticket_schema import TicketSchema
from datetime import datetime
from functools import wraps
from app.extensions import db

ticket_bp = Blueprint('ticket', __name__, url_prefix='/tickets')

ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)

# Role-based access decorator
def role_required(allowed_roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("role", None)
            if user_role not in allowed_roles:
                return jsonify(msg="Forbidden: You do not have access to this resource"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

@ticket_bp.route('', methods=['POST'])
@jwt_required()
def create_ticket():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"msg": "No input data provided"}), 400

    errors = ticket_schema.validate(json_data)
    if errors:
        # Return 422 Unprocessable Entity for validation errors
        return jsonify({"errors": errors}), 422

    ticket = ticket_schema.load(json_data)  # This returns a Ticket instance now
    ticket.user_id = get_jwt_identity()  # assign user_id manually

    db.session.add(ticket)
    db.session.flush()  # To get ticket.id before commit

    audit = AuditLog(
        action="create_ticket",
        timestamp=datetime.utcnow(),
        actor_id=ticket.user_id,
        ticket_id=ticket.id
    )
    db.session.add(audit)
    db.session.commit()

    result = ticket_schema.dump(ticket)
    return jsonify(result), 201

# GET Tickets
@ticket_bp.route('', methods=['GET'])
@jwt_required()
def get_tickets():
    user_id = get_jwt_identity()
    claims = get_jwt()
    user_role = claims.get("role", None)

    if user_role == 'admin':
        tickets = Ticket.query.all()
    else:
        tickets = Ticket.query.filter_by(user_id=user_id).all()

    return jsonify(tickets_schema.dump(tickets)), 200

# UPDATE Ticket
@ticket_bp.route('/<int:ticket_id>', methods=['PUT'])
@jwt_required()
def update_ticket(ticket_id):
    user_id = int(get_jwt_identity())  
    claims = get_jwt()
    user_role = claims.get("role", None)

    ticket = db.session.get(Ticket, ticket_id)
    if not ticket:
        return jsonify({"msg": "Ticket not found"}), 404

    #  Allow update only if owner or admin
    if ticket.user_id != user_id and user_role != 'admin':
        return jsonify({"msg": "Forbidden: You can only update your own tickets"}), 403

    data = request.get_json() or {}
    if "title" in data:
        ticket.title = data["title"]
    if "description" in data:
        ticket.description = data["description"]
    if "priority" in data:
        ticket.priority = data["priority"]
    if "status" in data:
        ticket.status = data["status"]

    audit = AuditLog(
        action="update_ticket",
        timestamp=datetime.utcnow(),
        actor_id=user_id,
        ticket_id=ticket.id
    )
    db.session.add(audit)
    db.session.commit()

    return jsonify({"msg": "Ticket updated successfully", "id": ticket.id}), 200

# DELETE Ticket
@ticket_bp.route('/<int:ticket_id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin'])
def delete_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"msg": "Ticket not found"}), 404

    db.session.delete(ticket)

    user_id = get_jwt_identity()
    audit = AuditLog(
        action="delete_ticket",
        timestamp=datetime.utcnow(),
        actor_id=user_id,
        ticket_id=ticket.id
    )
    db.session.add(audit)
    db.session.commit()

    return jsonify({"msg": "Ticket deleted successfully", "id": ticket.id}), 200
