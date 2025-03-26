from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from apps.auth.models import User
from apps.passwords.models import PasswordEntry
from apps.passwords.passwordserviceinterface import PasswordServiceInterface
from helpers.passwordsHandler import encrypt_password, decrypt_password
from mongoengine.errors import DoesNotExist


class PasswordsService(PasswordServiceInterface):
    def save_credentials(self, user_identity, data):

        if not isinstance(user_identity, str):
            return jsonify({f"status": "error", "message": "Invalid token data"}), 400

        email =  user_identity
        if not email:
            return jsonify({f"status": "error", "message": "Email missing from token"}), 400

        website = data['website']
        username = data['username']
        password = data['password']

        try:
            user = User.objects.get(email=email)


            encrypted_password = encrypt_password(email, password)

            stored_password_entry = PasswordEntry.objects(user=user, website=website).first()
            if stored_password_entry:
                return jsonify({'status': "error",
                                'message': "credentials already saved"}), 401

            new_password_entry = PasswordEntry(
                user=user,
                website=website,
                username=username,
                encrypted_password=encrypted_password,
            )
            new_password_entry.save()
            return jsonify({'status': "success",
                            'message': "credentials successfully saved",}), 201
        except DoesNotExist:
            return jsonify({'status': "error",
                            'message': "credentials not found",}), 404



    def retrieve_credentials(self, user_identity):
        email = user_identity
        if not email:
            return jsonify({f"status": "error", "message": "Email missing from token"}), 400

        try:

            user = User.objects.get(email=email)

            stored_password = PasswordEntry.objects(user=user)
            if not stored_password:
                return jsonify({f"status": "error",
                                "message": "No credential saved yet"}), 404

            credentials_list = [
                {
                    "website": entry.website,
                    "username": entry.username,
                    "password": decrypt_password(email, entry.encrypted_password),
                }

                for entry in stored_password
            ]

            return jsonify({'status': "success",
                            'credentials': credentials_list,}), 201
        except Exception as e:
            return jsonify({'status': "error",
                            'message': str(e)}), 500







    def delete_credentials(self, data):
        pass