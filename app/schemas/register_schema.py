from app.extensions import ma
from marshmallow import fields, validate, validates, ValidationError
import re

class RegisterSchema(ma.Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True, validate=validate.Length(max=120))
    password = fields.Str(required=True, validate=validate.Length(min=6))
    role = fields.Str(required=True, validate=validate.OneOf(["user", "admin"]))

    @validates("username")
    def validate_username(self, value, **kwargs):
        if not re.match(r'^[A-Za-z0-9_.-]+$', value):
            raise ValidationError(
                "Username may only contain letters, numbers, dots, underscores, and hyphens."
            )
