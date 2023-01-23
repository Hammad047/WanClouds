from functools import wraps
from flask import Response, request


def validate_schema(schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()  # getting data from POSTMAN
            errors = schema.validate(data)
            if errors:
                return Response(str(errors), status=404)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
