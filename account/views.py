from django.shortcuts import render
from .serializers import RegistrationSerializer, LoginSerializer
from .models import User

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .renderers import UserJSONRenderer

# 회원가입
class UserCreate(generics.CreateAPIView):
    permission_classes = (AllowAny,) #누가 이 view를 사용할 수 있는지에 대한 범위를 결정
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)
    def post(self, request):
        user = request.data
        
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    #queryset = User.objects.all()

# class SuperuserCreate(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# 로그인은 rest_framework에서 제공하는 기능 활용 가능
# but JWT token으로 사용자 구분하기

class LoginAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer
    
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)