from django.shortcuts import render
from .serializers import UserSerializer
from .models import User
from rest_framework import generics

# 회원가입
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# class SuperuserCreate(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# 로그인은 rest_framework에서 제공하는 기능 활용 가능
# but JWT token으로 사용자 구분하기