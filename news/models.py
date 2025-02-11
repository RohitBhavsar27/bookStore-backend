from django.db import models
from mongoengine import *
import datetime


# Create your models here.
class News(Document):
    title = StringField(required=True, max_length=200)
    description = StringField(required=True, max_length=200)
    image = StringField(required=True, max_length=200)

    def __str__(self):
        return f"{self.title}, {self.description}, {self.coverImage}"

    meta = {
        "collection": "news",  # Name of the collection in MongoDB
    }
