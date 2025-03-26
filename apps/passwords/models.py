from mongoengine import Document, StringField, BinaryField, ReferenceField

from apps.auth.models import User


class PasswordEntry(Document):
    user=ReferenceField(User, required=True, reverse_delete_rule=2)
    website=StringField(required=True)
    encrypted_password=BinaryField(required=True)