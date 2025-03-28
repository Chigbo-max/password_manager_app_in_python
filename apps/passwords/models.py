import datetime

from mongoengine import Document, StringField, BinaryField, ReferenceField, DateTimeField

from apps.auth.models import User


class CredentialsEntry(Document):
    user=ReferenceField(User, required=True, reverse_delete_rule=2)
    website=StringField(required=True)
    username=StringField(required=True)
    encrypted_password=BinaryField(required=True)
    timestamp = DateTimeField(default=datetime.datetime.now(), required=True)
