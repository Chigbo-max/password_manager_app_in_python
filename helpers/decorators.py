from functools import wraps

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from apps.auth.models import User


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_identity = get_jwt_identity()

        email = user_identity

        user = User.objects(email=email).first()
        if not user or user.role != "admin":
            return jsonify({"status": "error", "message": "Admin access required"}), 403

        return func(*args, **kwargs)

    return wrapper