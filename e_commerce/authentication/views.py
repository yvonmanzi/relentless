from django.shortcuts import render
from rest_framework import viewsets

from rest_framework import generics, status
from django.contrib.auth.models import User
from rest_framework.response import Response

# TODO: Check why this is or is not working
from rest_framework_simplejwt.tokens import RefreshToken


from authentication.serializers import LoginSerializer, RegisterSerializer

# Create your views here.


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validate_data()
        refresh = RefreshToken.for_user(user)
        return Response({"refresh": str(refresh), "access": str(refresh.access_token)})
