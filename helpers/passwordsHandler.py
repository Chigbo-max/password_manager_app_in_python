
from cryptography.fernet import Fernet
from flask import jsonify

from apps.auth.models import User


def get_user_key(user_id):
    try:
        user=User.objects(email=user_id).first()
        if user is None:
            return jsonify(f"No encryption key found for: {user_id}"), 401
        return user.encryption_key
    except Exception as e:
        return jsonify(f"Error getting encryption key for: {user_id}: {e}"), 401

def encrypt_password(user_id, password):
    try:
        key = get_user_key(user_id)
        cipher = Fernet(key)
        encrypted_password = cipher.encrypt(password.encode())
        return encrypted_password
    except Exception as e:
        return jsonify(f"Error encrypting password for: {user_id}: {e}"), 401

def decrypt_password(user_id, encrypted_password):
    try:
        key = get_user_key(user_id)
        cipher = Fernet(key)
        decrypted_password = cipher.decrypt(encrypted_password)
        return decrypted_password.decode()
    except Exception as e:
        return jsonify(f"Error decrypting password for: {user_id}: {e}"), 401



