import traceback

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from apps.auth.models import User
from apps.auth.services import AuthService



auth_service = AuthService()

auth_view = Blueprint('auth_view', __name__)


@auth_view.route('/register', methods=['POST'])
def register():
    return auth_service.register(request.get_json())


@auth_view.route('/login', methods=['POST'])
def login():
    return auth_service.login(request.get_json())

@auth_view.route('/forget-password', methods=['POST'])
def forget_password():
    return auth_service.forget_password(request.get_json())

@auth_view.route('/reset-password-confirm', methods=['POST'])
def reset_password():
    return auth_service.reset_password(request.get_json())

@auth_view.route("/get-user-email", methods=["GET"])
@jwt_required()
def get_user_email():
    try:
        email = get_jwt_identity()
        return jsonify({"email": email}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@auth_view.route("/get-user", methods=["GET"])
@jwt_required()
def get_user():
    try:
        current_user =  get_jwt_identity()
        user = User.objects.get(email=current_user)

        user_list= {
                "email": str(user.email),
                "role": str(user.role),
                "status": str(user.status.value),
            }

        return jsonify({"status": "success", "message": user_list}), 200

    # except User.DoesNotExist:
    #     return jsonify({"error": "User does not exist"}), 404
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500


