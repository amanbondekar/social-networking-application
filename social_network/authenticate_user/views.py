from django.shortcuts import render
from .models import CustomUser
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializer import SignupSerializer, LoginSerializer, CustomUserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            try:
                validate_email(email)  # Validate email format
            except ValidationError:
                return Response({'error': 'Invalid email format'}, status=400)
            
            if CustomUser.objects.filter(email=email.lower()).exists():
                return Response({'error': 'Email already exists'}, status=400)
            else:
                # Create an instance of your custom user model
                user = CustomUser.objects.create_user(email=email.lower(), password=password)
                return Response({'message': 'Signup successful'})
        return Response(serializer.errors, status=400)

    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Authenticate user
        user = CustomUser.objects.filter(email=email).first()
        if user is not None:
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({
                'message': 'Login successful',
                'access_token': access_token,
                'refresh_token': str(refresh)
            })
        else:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = CustomUser.objects.get(id=request.user.id)
        serializer = CustomUserSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request):
        user_profile = CustomUser.objects.get(id=request.user.id)
        serializer = CustomUserSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)