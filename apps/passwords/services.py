import traceback

from flask import request

from apps.admin.models import AuditLog


from flask import jsonify
from werkzeug.security import check_password_hash

from apps.auth.models import User
from apps.passwords.models import CredentialsEntry
from apps.passwords.passwordserviceinterface import PasswordServiceInterface
from helpers.passwordsHandler import encrypt_password, decrypt_password
from mongoengine.errors import DoesNotExist


class PasswordsService(PasswordServiceInterface):
    def save_credentials(self, user_identity, data):

        if not isinstance(user_identity, str):
            return jsonify({"status": "error", "message": "Invalid token data"}), 400

        email =  user_identity
        if not email:
            return jsonify({"status": "error", "message": "Email missing from token"}), 400

        website = data['website']
        username = data['username']
        password = data['password']

        try:
            user = User.objects.get(email=email)


            encrypted_password = encrypt_password(email, password)

            stored_password_entry = CredentialsEntry.objects(user=user, website=website).first()
            if stored_password_entry:
                return jsonify({'status': "error",
                                'message': "credentials already saved"}), 401

            new_password_entry = CredentialsEntry(
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


    def save_detected_credentials(self, user_identity, data):
        email = user_identity

        website = data['website']
        username = data['username']
        password = data['password']

        try:
            user = User.objects(email=email).first()

            if not user:
                return jsonify({f"status": "error",
                            "message": "User does not exist"}), 404


            credentials_entry = CredentialsEntry(user=user, website=website, username=username,
                                          encrypted_password=encrypt_password(email, password))
            credentials_entry.save()

            return jsonify({'status': "success",
                        'message': "credentials successfully saved",}), 201
        except DoesNotExist:
            return jsonify({'status': "error",
                            'message': "credentials not found",}), 404


    def retrieve_credentials(self, user_identity):
        email = user_identity
        if not email:
            return jsonify({"status": "error", "message": "Email missing from token"}), 400

        try:

            user = User.objects.get(email=email)

            stored_password = CredentialsEntry.objects(user=user)
            if not stored_password:
                return jsonify({"status": "error",
                                "message": "No credential saved yet"}), 404

            credentials_list = []

            for entry in stored_password:
                try:
                    decrypted_password = decrypt_password(email, entry.encrypted_password)
                    credentials_list.append({
                    "website": entry.website,
                    "username": entry.username,
                    "password": decrypted_password
                    })
                except Exception as e:
                    print(f"Decryption failed for {entry.website}: {e}")
                    traceback.format_exc()
                    credentials_list.append({
                        "website": entry.website or "unknown",
                        "username": entry.username,
                        "password": "[Decryption Failed]"
                    })
            return jsonify({"status": "success",
                            "credentials": credentials_list,}), 200
        except Exception as error:
            print(traceback.format_exc())
            return jsonify({"status": "error",
                        "message": str(error)}), 500



    def delete_credentials(self, user_identity, website):
        email = user_identity
        if not email:
            return jsonify({"status": "error", "message": "Email missing from token"}), 400

        try:
            user = User.objects.get(email=email)
            if not user:
                return jsonify({"status": "error", "message": "User not found"}), 404

            credentials_entry = CredentialsEntry.objects(user=user, website=website).first()
            if not credentials_entry:
                return jsonify({"status": "error",
                                "message": "No credential saved yet"}), 404
            credentials_entry.delete()


            log_entry = AuditLog(
                user=user,
                email=user.email,
                action= "delete",
                details=f"deleted credentials for {website}",
                ip_address= request.remote_addr,
                device_info= request.user_agent.string,
            )
            log_entry.save()

            return jsonify({'status': "success",
                            'message': "credentials successfully deleted"
                 }), 200
        except Exception as e:
            return jsonify({'status': "error",
                            'message': str(e)}), 500


    def update_credentials(self, user_identity, data, website):
        email = user_identity

        try:


            user = User.objects.get(email=email)

            if not user:
                return jsonify({"status": "error",
                                "message": "User does not exist"}), 404

            master_password = data.get('master_password')

            if not user.master_password:
                return jsonify({"status": "error", "message": "Master password is required for this action"}), 500

            if not check_password_hash(user.master_password, master_password):
                return jsonify({"status": "error",
                                "message": "Password incorrect"}), 401


            saved_credentials = CredentialsEntry.objects(user=user, website=website).first()

            if not saved_credentials:
                return jsonify({"status": "error",
                                "message": "No credential saved yet"}), 404

            new_password = data.get('new_password')
            if new_password:
                new_encrypted_password = encrypt_password(email, new_password)
                saved_credentials.encrypted_password = new_encrypted_password

            if "new_website" in data:
                saved_credentials.website = data['new_website']

            if "new_username" in data:
                saved_credentials.username = data['new_username']

            saved_credentials.save()

            log_entry = AuditLog(
                user=user,
                action="update",
                details=f"updated credentials for {website}",
                ip_address=request.remote_addr,
                device_info=request.user_agent.string,
            )

            log_entry.save()

            return jsonify({'status': "success",
                            'message': "credentials successfully updated",
                            'new_credentials':{
                                "website": saved_credentials.website,
                                "username": saved_credentials.username,
                            }
                            }), 200
        except Exception as e:
            print(traceback.format_exc())
            return jsonify({'status': "error",
                            'message': str(e)}), 500











