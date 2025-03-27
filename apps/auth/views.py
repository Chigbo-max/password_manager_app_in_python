from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from apps.auth.services import AuthService



auth_service = AuthService()

auth_view = Blueprint('auth_view', __name__)


@auth_view.route('/register', methods=['POST'])
def register():
    return auth_service.register(request.get_json())


@auth_view.route('/login', methods=['POST'])
def login():
    return auth_service.login(request.get_json())

@auth_view.route('/reset-password', methods=['POST'])
@jwt_required
def reset_password():
    return auth_service.reset_password(request.get_json())

@auth_view.route('/reset-password-confirm', methods=['POST'])
def reset_password_confirm():
    return auth_service.reset_password_confirm(request.get_json())

@auth_view.route("/get-user-email", methods=["GET"])
@jwt_required()
def get_user_email():
    try:
        email = get_jwt_identity()
        return jsonify({"email": email}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


