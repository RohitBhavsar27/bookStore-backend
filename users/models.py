import bcrypt
from mongoengine import *


class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(choices=["user", "admin"], required=True)

    def hash_password(self):
        self.password = bcrypt.hashpw(
            self.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def save(self, *args, **kwargs):
        if not self.password.startswith("$2b$"):  # Ensure password is hashed only once
            self.hash_password()
        super(User, self).save(*args, **kwargs)

    meta = {
        "collection": "users",  # Name of the collection in MongoDB
    }


# admin = User(username="admin123", password="securepassword", role="admin")
# admin.save()


