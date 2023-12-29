from mongoengine import Document, StringField, FloatField, ReferenceField, DateTimeField
from .user import User


class Transaction(Document):
    user = ReferenceField(User, required=True)
    type = StringField(required=True, choices=['income', 'expense'])
    amount = FloatField(required=True)
    description = StringField()
    date = DateTimeField()
