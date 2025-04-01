import base64
import secrets

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from apps.passwords.models import CredentialsEntry
from helpers.passwordsHandler import encrypt_password


def generate_token():
    return secrets.token_urlsafe(32)


def derive_encryption_key(master_password: str, salt: bytes) -> str:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode())).decode()

def auto_save_credentials(user, email, master_password):
    encrypted_password = encrypt_password(email, master_password)
    CredentialsEntry(user=user, username=email, encrypted_password=encrypted_password).save()