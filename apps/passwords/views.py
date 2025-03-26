from flask import Blueprint, request
import logging
from flask_jwt_extended import get_jwt_identity, jwt_required

from apps.passwords.services import PasswordsService

password_manager_view = Blueprint('password_manager_view', __name__)

password_service = PasswordsService()


@password_manager_view.route('/save-credentials', methods=['POST'])
@jwt_required()
def save_credentials():
    data = request.get_json()
    user_identity = get_jwt_identity()
    return password_service.save_credentials(user_identity, data)