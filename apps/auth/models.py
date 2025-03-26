from datetime import datetime

from mongoengine import Document, StringField, EmailField, DateTimeField, EnumField, BinaryField

from apps.auth.status import AccountStatus


class User(Document):
    email = EmailField(required=True, unique=True)
    master_password = StringField(max_length=180, min_length=8, required=True)
    encryption_key = StringField(required=True)
    salt = BinaryField()
    role = StringField(choices=['admin', 'user'], default='user')
    status = EnumField(AccountStatus, default=AccountStatus.ACTIVE)
    reset_token = StringField(max_length=128)
    created_at = DateTimeField(default=datetime.now)