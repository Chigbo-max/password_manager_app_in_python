import datetime

from mongoengine import Document, StringField, BinaryField, ReferenceField, DateTimeField, EmailField

from apps.auth.models import User


class CredentialsEntry(Document):
    user=ReferenceField(User, required=True, reverse_delete_rule=2)
    email=EmailField(required=False)
    website=StringField(required=False)
    username=StringField(required=False)
    encrypted_password=BinaryField(required=True)
    timestamp = DateTimeField(default=datetime.datetime.now())
