import re
from marshmallow import fields, validates, ValidationError
from flask_marshmallow import Marshmallow

ma = Marshmallow()


class UserSchema(ma.Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @validates("name")
    def validate_name(self, value):
        if "name" in value:
            raise ValidationError("Name cannot contain the word 'name'.")
        if not re.match("^[A-Z].*", value):
            raise ValidationError("The first letter of the name must be uppercase.")
        if not re.match("^[a-zA-Z0-9_]+$", value):
            raise ValidationError("Name can only contain letters, numbers, and underscores.")
        if len(value) < 3:
            raise ValidationError("Minimum length of name must be 3.")

    @validates("email")
    def validate_email(self, value):
        if not re.match(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+.[A-Z|a-z]{2,}", value):
            raise ValidationError("Please recheck your email.")

    @validates("password")
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not any(p.isupper() for p in value):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not any(p.isdigit() for p in value):
            raise ValidationError("Password must contain at least one number.")
