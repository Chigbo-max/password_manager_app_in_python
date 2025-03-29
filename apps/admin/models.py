import datetime

from mongoengine import ReferenceField, StringField, DateTimeField, Document, EmailField

from apps.auth.models import User


class AuditLog(Document):

    user= ReferenceField(User, required=False)
    email=EmailField(required=True)
    action= StringField(required=True)
    details= StringField(required=True)
    ip_address= StringField(required=True)
    device_info= StringField(required=True)
    timestamp= DateTimeField(default=datetime.datetime.now)
