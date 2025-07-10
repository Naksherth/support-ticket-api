from datetime import datetime
from app.extensions import db

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text)

    actor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'))
