from functools import wraps
from rest_framework.response import Response
from rest_framework import status
import jwt
import os

JWT_SECRET = os.getenv("JWT_SECRET_KEY", "your_secret_key")


def verify_admin_token(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response(
                {"message": "Access Denied. No token provided"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token = auth_header.split(" ")[1]

        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            if decoded_token.get("role") != "admin":
                return Response(
                    {"message": "Access Denied. Admins only."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            request.user = decoded_token  # ✅ Store decoded user data in request
            return view_func(request, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return Response(
                {"message": "Token expired"}, status=status.HTTP_403_FORBIDDEN
            )

        except jwt.InvalidTokenError:
            return Response(
                {"message": "Invalid token"}, status=status.HTTP_403_FORBIDDEN
            )

    return wrapper
