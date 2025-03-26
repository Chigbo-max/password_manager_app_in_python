from mongoengine import Document, StringField


class EncryptionKey(Document):
    user_id = StringField(required=True, unique=True)
    secret_key = StringField(required=True)
