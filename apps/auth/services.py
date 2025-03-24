import traceback
from datetime import timedelta

from flask import request, jsonify
from flask_jwt_extended import create_refresh_token, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from apps.auth.authInterface import AuthInterface
from helpers import Utiility

from apps.auth.models import User
from helpers.config import Config


class AuthService(AuthInterface):


    def register(self,data):
        try:
            # data = request.get_json()
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
            # data = request.get_json()
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
       pass




    def logout(self, data):
        pass




