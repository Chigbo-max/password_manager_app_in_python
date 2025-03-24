from datetime import datetime

from mongoengine import Document, StringField, EmailField, DateTimeField


class User(Document):
    email = EmailField(required=True, unique=True)
    master_password = StringField(max_length=180, min_length=8, required=True)
    created_at = DateTimeField(default=datetime.now)