from .models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(
            # email = validated_data['email'],
            # nickname = validated_data['nickname'],
            # name = validated_data['name'],
            # password = validated_data['password']
            login_id = validated_data['login_id'],
            login_password = validated_data['login_password'],
            user_nickname = validated_data['user_nickname'],
            current_address = validated_data['current_address'],
            payment_method = validated_data['payment_method'],
            user_phone = validated_data['user_phone'],
            user_allergy = validated_data['user_allergy']
        )
    class Meta:
        model = User
        # fields = ['nickname', 'email', 'name', 'password']
        fields = ['login_id', 'login_password', 'user_nickname', 'current_address', 'payment_method', 'user_phone', 'user_allergy']
