import traceback
from datetime import timedelta

from flask import request, jsonify
from flask_jwt_extended import create_refresh_token, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from apps.auth.authInterface import AuthInterface
from helpers import Utility

from apps.auth.models import User
from helpers.config import Config
from helpers.gmailservice import GmailService


class AuthService(AuthInterface):


    def register(self,data):
        try:
            if User.objects(email=data['email']).first():
                return jsonify({"message": f"User {data['email']} is already registered"})

            user = User(
                email=data['email'].strip().lower(),
                master_password= generate_password_hash(data['master_password'])
                ).save()

            access_token = create_access_token(identity=user.email, expires_delta=timedelta(days=1))
            refresh_token = create_refresh_token(identity=user.email, expires_delta=timedelta(days=1))


            return jsonify({"status": "success",
                            "message": f"{user.email} registered successfully",
                            "access_token": access_token,
                            "refresh_token": refresh_token,
                            }), 201
        except Exception as e:
            print("Registration Error:", traceback.format_exc())  # Debugging
            return jsonify({"status": "error",
                            "message": f"registration unsuccessful {e}"}), 500


    def login(self, data):

        try:
            email = data['email'].strip().lower()
            master_password = data['master_password'].strip()

            user = User.objects(email=email).first()
            if user and check_password_hash(user.master_password, master_password):
                access_token = create_access_token(identity=user.email, expires_delta=timedelta(minutes=30))
                refresh_token = create_refresh_token(identity=user.email)

                return jsonify({"status": "success",
                                "message": f"{user.email} logged in successfully",
                                "access_token": access_token,
                                "refresh_token": refresh_token,
                                }), 200
            print("Login error:", traceback.format_exc())
            return jsonify({"status": "error",
                            "message": f"login unsuccessful, please register"}), 401
        except Exception as e:
            return jsonify({"status": "error",
                            "message": f"login unsuccessful {e}"}), 500


    def reset_password(self, data):

       try:
           email = data['email'].strip().lower()
           user = User.objects(email=email).first()

           if not user:
               return jsonify({"message": f"User {data['email']} is not registered"})

           reset_token = Utility.generate_token()
           reset_link = f"{Config.FRONTEND_URI}/reset-password?token={reset_token}"

           user.update(set__reset_token=reset_token)

           email_service = GmailService()

           email_sent = email_service.send_email(
               to_email=user.email,
               subject=f"Password Reset for {user.email}",
               message=f"<p>Click the following link to reset your password: <a href = '{reset_link}'>{reset_link}</a></p>",
           )

           if email_sent:
               return jsonify({"status": "success",
                               "message": f"Password reset mail sent to {user.email} successfully"}), 201
           return jsonify({"status": "error",
                           "message": f"password reset mail failed to send, please try again"}), 401
       except Exception as e:
           return jsonify({"status": "error",
                           "message": f"password reset unsuccessful {e}"}), 500


    def reset_password_confirm(self, data):
        try:
            reset_token = data.get('reset_token')
            new_password = data.get('new_password')

            if not reset_token or not new_password:
                return jsonify({"message": f"password reset unsuccessful, please try again"}), 401

            user = User.objects(reset_token=reset_token).first()

            if not user:
                return jsonify({"message": "Invalid or expired token"}), 401

            user.update(set__master_password=generate_password_hash(new_password),
            set__reset_token=None)

            return jsonify({"status": "success", "message": f"password reset successfully"}), 201

        except Exception as e:
            return jsonify({"status": "error",
                            "message": f"password reset unsuccessful {e}"}), 500


    def logout(self, data):
        pass




