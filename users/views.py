from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import jwt
import os
from datetime import datetime, timedelta
from users.models import User

JWT_SECRET = os.getenv("JWT_SECRET_KEY", "your_secret_key")


@api_view(["POST"])
def admin_login(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")

        admin = User.objects(username=username).first()

        if not admin:
            return Response(
                {"message": "Admin not found!"}, status=status.HTTP_404_NOT_FOUND
            )

        if not admin.check_password(password):
            return Response(
                {"message": "Invalid password!"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # ✅ Generate JWT token
        token_payload = {
            "id": str(admin.id),
            "username": admin.username,
            "role": admin.role,
            "exp": datetime.utcnow() + timedelta(hours=1),
        }
        token = jwt.encode(token_payload, JWT_SECRET, algorithm="HS256")

        return Response(
            {
                "message": "Authentication successful",
                "token": token,
                "user": {"username": admin.username, "role": admin.role},
            },
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        print("Failed to login as admin:", e)
        return Response(
            {"message": "Failed to login as admin"}, status=status.HTTP_401_UNAUTHORIZED
        )


from rest_framework.decorators import api_view
from rest_framework.response import Response
from middleware.jwt_middleware import verify_admin_token


@api_view(["GET"])
@verify_admin_token
def admin_dashboard(request):
    return Response({"message": "Welcome to Admin Dashboard", "user": request.user})


