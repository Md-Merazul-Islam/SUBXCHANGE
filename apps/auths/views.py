from.tokens import CustomRefreshToken
from rest_framework import generics, status
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, LoginSerializer
from ..core.response import  success_response,failure_response
from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return success_response(
                message="User registered successfully",
                data={
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "access_token": access_token,
                    "refresh_token": refresh_token
                },
                status=status.HTTP_201_CREATED
            )
        return failure_response("Registration failed", error=serializer.errors)
          
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            refresh = CustomRefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response_data = {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
            login(request, user)
            return success_response("Login successful", response_data)

        return failure_response("Login failed", {}, error=serializer.errors)
