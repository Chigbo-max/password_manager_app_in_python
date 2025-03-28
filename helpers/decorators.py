from functools import wraps

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from apps.auth.models import User


def admin_required(param):
    @wraps(param)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_identity = get_jwt_identity()

        user = User.objects(email=user_identity).first()
        if not user or user.role != "admin":
            return jsonify({"status": "error", "message": "Admin access required"}), 403

        return param(*args, **kwargs)

    return wrapper