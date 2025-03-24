from flask import Blueprint, request
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
def reset_password():
    return auth_service.login(request.get_json())



