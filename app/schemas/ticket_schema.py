from app.extensions import ma
from app.models import Ticket
from marshmallow import validate

class TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ticket
        load_instance = True
        include_fk = True 

    id = ma.auto_field(dump_only=True)
    title = ma.auto_field(required=True, validate=validate.Length(min=5))
    description = ma.auto_field(required=True, validate=validate.Length(min=10))
    priority = ma.auto_field(load_default="medium", validate=validate.OneOf(["low", "medium", "high"]))
    status = ma.auto_field(dump_only=True)
    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)
    user_id = ma.auto_field(dump_only=True)
