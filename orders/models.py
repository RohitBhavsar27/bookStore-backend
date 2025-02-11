from django.db import models
from mongoengine import *
import datetime

from books.models import Books


# Create your models here.
class Address(EmbeddedDocument):
    street = StringField(required=True, max_length=255)
    city = StringField(required=True, max_length=100)
    country = StringField(required=True, max_length=100)
    state = StringField(required=True, max_length=100)
    zipcode = StringField(required=True, max_length=20)


class Orders(Document):
    name = StringField(required=True, max_length=100)
    email = StringField(required=True, max_length=255)
    phone = StringField(required=True, max_length=20)
    address = EmbeddedDocumentField(Address)  # Embedded Address Document
    productIds = ListField(ReferenceField(Books), required=True)  # Reference to Book documents
    totalPrice = FloatField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))

    meta = {
        "collection": "orders",  # Name of the collection in MongoDB
    }
