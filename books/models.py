from django.db import models
from mongoengine import *
import datetime


# Create your models here.
class Books(Document):
    title = StringField(required=True, max_length=200)
    description = StringField(required=True, max_length=200)
    category = StringField(required=True, max_length=200)
    trending = BooleanField(default=False)
    coverImage = StringField(required=True, max_length=200)
    oldPrice = FloatField(required=True)
    newPrice = FloatField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))

    def save(self, *args, **kwargs):
        # Update `updated_at` field to current time on every save
        self.updated_at = datetime.datetime.utcnow()
        return super(Books, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}, {self.description}, {self.category}, {self.newPrice}, {self.oldPrice}, {self.trending}, {self.coverImage}"

    meta = {
        "collection": "books",  # Name of the collection in MongoDB
    }
