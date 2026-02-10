from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .serializers import UserSignupSerializer

from rest_framework import generics,permissions



class SignupView(generics.CreateAPIView):
    """Signup view with overiding permission classes"""

    serializer_class=UserSignupSerializer
    permission_classes=[permissions.AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

