from mongoengine import Document, StringField, BinaryField


class PasswordEntry(Document):
    user_id=StringField(unique=True, required=True)
    website=StringField(required=True)
    username=StringField(required=True)
    encrypted_password=BinaryField(required=True)