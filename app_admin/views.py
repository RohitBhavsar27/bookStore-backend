from django.shortcuts import render
import bcrypt

# Create your views here.


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
 

# Example usage
password = "mysecretpassword"
hashed_password = hash_password(password)

# Store the hashed_password in the database

# To verify a password:
if check_password("mysecretpassword", hashed_password):
    print("Password is valid")
else:
    print("Invalid password")
