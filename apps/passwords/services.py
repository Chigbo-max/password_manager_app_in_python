import base64
import os

from cryptography.fernet import Fernet
from flask import jsonify

from apps.passwords.models.encryptionkey_model import EncryptionKey


def generate_key(user_id):
   key=base64.urlsafe_b64encode(os.urandom(32)).decode()
   EncryptionKey(user_id=user_id, secret_key=key).save()
   return keyd

def get_user_key(user_id):
    key_entry=EncryptionKey.objects(user_id=user_id).first()
    if key_entry is None:
        return jsonify(f"No encryption key found for: {user_id}"), 401
    return key_entry.secret_key.encode()

def encrypt_password(user_id, password):
    key = get_user_key(user_id)
    cipher = Fernet(key)
    encrypted_password = cipher.encrypt(password.encode())
    return encrypted_password

def decrypt_password(user_id, encrypted_password):
    key = get_user_key(user_id)
    cipher = Fernet(key)
    decrypted_password = cipher.decrypt(encrypted_password)
    return decrypted_password.decode()



