from django.shortcuts import render
from .models import User
from .serializers import (   
    RegistrationSerializer, LoginSerializer, UserSerializer
)

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework import generics
from .renderers import UserJSONRenderer
from rest_framework.generics import RetrieveUpdateAPIView

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


# 로그인은 rest_framework에서 제공하는 기능 활용 가능
# but JWT token으로 사용자 구분하기

class LoginAPIView(generics.CreateAPIView ):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer
    
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# User 정보 Update View
class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer
    
    # RetrieveUpdateAPIView에서 제공하는 get method
    def get(self, request, *args, **kwargs):
        # 단순 'User' 객체를 client에게 보내주기 위한 serializer
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 객체를 업데이트 할 때 부분 업데이트가 가능한 method 
    def patch(self, request, *args, **kwargs):
        serializer_data = request.data
        # instance, validated_data를 serializer에 전달함 
        # validated_data는 serializer_data
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True #부분 업데이트 가능
        )
        
        serializer.is_valid(raise_exception=True)
        #업데이트 된 instance(사용자 정보) DB에 저장
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)