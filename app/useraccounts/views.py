from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .serializers import UserSignupSerializer
import logging
from rest_framework import generics,permissions

logger = logging.getLogger(__name__)

class SignupView(generics.CreateAPIView):
    """Signup view with overiding permission classes"""

    serializer_class=UserSignupSerializer
    permission_classes=[permissions.AllowAny]


    def perform_create(self, serializer):
        user = serializer.save()
        logger.info(
            "User signed up",
            extra={
                "event": "USER_SIGNUP",
                "user_id": user.id,
                "email": user.email,
            },
        )

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

