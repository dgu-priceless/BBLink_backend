from .models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model

from django.contrib.auth import authenticate
from django.utils import timezone

#https://axce.tistory.com/108
#ers.ModelSerializer를 상속받아 RegistrationSerializer 생성
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length = 128,
        min_length = 8,
        write_only = True #password를 updating, creating 할 때는 사용되지만, serializing 할 때는 포함되지 않도록 하기 위함
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # fields = ['nickname', 'email', 'name', 'password']
        fields = [
            'user_id',
            'login_id', 
            'password', 
            'user_nickname', 
            'current_address', 
            'payment_method', 
            'user_phone', 
            'user_allergy', 
            'token']

    def create(self, validated_data):
        # user = User.objects.create_user(
        #     email = validated_data['email'],
        #     nickname = validated_data['nickname'],
        #     name = validated_data['name'],
        #     password = validated_data['password']
        #     user_id = validated_data['user_id'],
        #     login_id = validated_data['login_id'],
        #     password = validated_data['password'],
        #     user_nickname = validated_data['user_nickname'],
        #     current_address = validated_data['current_address'],
        #     payment_method = validated_data['payment_method'],
        #     user_phone = validated_data['user_phone'],
        #     user_allergy = validated_data['user_allergy']
        # )
        user = User.objects.create_user(**validated_data)
        return user
       


class LoginSerializer(serializers.Serializer):
    # 1.
    login_id = serializers.CharField(max_length=45)
    password = serializers.CharField(max_length=200, write_only=True)
    last_login = serializers.CharField(max_length=255, read_only=True)
    
    # 2.
    def validate(self, data):
        login_id = data.get('login_id', None)
        password = data.get('password', None)
        
        # 3.
        if login_id is None:
            raise serializers.ValidationError(
                'An id address is required to log in.'
            )
        
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        
        # 4.
        user = authenticate(login_id=login_id, password=password)
        
        # 5.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found'
            )
        
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        
        # 6.
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        # 7.
        return {
            'login_id': user.login_id,
            'last_login': user.last_login
        }

#사용자 정보(내 정보) 확인 및 업데이트할 때 사용할 serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=200,
        min_length=8,
        write_only=True #쓰기 옵션만 활성화
    )
    
    class Meta:
        model = User
        fields = [
            'user_id',
            'login_id', 
            'password', 
            'user_nickname', 
            'current_address', 
            'payment_method', 
            'user_phone', 
            'user_allergy', 
            'token'
        ]
    
        read_only_fields = ('token', )
        
    # 사용자의 정보를 업데이트 할 때 실행
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None) #password는 setattr로 변경하면XXX

        for (key, value) in validated_data.items():
            #password를 제외한 다른 key들의 value 값으로 현재 'User'의 속성값을 바꾸기
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password) #빼놓은 password를 수정한 부분이 있다면 '.set_password( )' 메소드 이용해 password 새롭게 설정함

        #변경된 instance의 정보를 저장 but DB에는 XX -> DB에 직접 저장하는 역할은 view의 serializer.save()에서 진행
        instance.save()
        return instance