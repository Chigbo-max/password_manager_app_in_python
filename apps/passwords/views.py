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

@password_manager_view.route('/retrieve-credentials', methods=['GET'])
@jwt_required()
def retrieve_credentials():
    user_identity = get_jwt_identity()
    return password_service.retrieve_credentials(user_identity)

@password_manager_view.route('/delete-credential/<website>', methods=['POST'])
@jwt_required()
def delete_credentials(website):
    user_identity = get_jwt_identity()
    return password_service.delete_credentials(user_identity, website)

@password_manager_view.route('/save-delete-credential', methods=['POST'])
@jwt_required()
def save_detected_credentials():
    user_identity = get_jwt_identity()
    data = request.get_json()
    return password_service.save_detected_credentials(user_identity, data)

