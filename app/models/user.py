from mongoengine import Document, StringField, EmailField, BooleanField


class User(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    hashed_password = StringField(required=True)
    is_admin = BooleanField(required=True, default=False)
