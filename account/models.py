from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator 

from django.db.models.fields import BooleanField
from core.models import TimestampedModel

import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.db import models

# 헬퍼 클래스
class UserManager(BaseUserManager):
    # 일반 user 생성
    def create_user(self, login_id, user_nickname, user_phone, current_address, payment_method, user_allergy, password=None):
        print(login_id)
        if not login_id: #로그인 아이디가 없다면
            raise ValueError('login_id는 필수 요소입니다.')
        if not user_nickname:
            raise ValueError('user nickname는 필수 요소입니다.')
        if not user_phone:
            raise ValueError('user_phone는 필수 요소입니다.')
        if not current_address:
            raise ValueError('current_address는 필수 요소입니다.')
        if not payment_method:
            raise ValueError('user payment_method는 필수 요소입니다.')
        if not password:            
           raise ValueError('user password는 필수 요소입니다.')

        user = self.model(
            login_id = login_id,
            user_nickname = user_nickname,
            user_phone = user_phone,
            current_address = current_address,
            payment_method = payment_method,
            user_allergy = user_allergy,
            #추가
            password = password
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 관리자 user 생성
    def create_superuser(self, login_id, user_nickname, password, current_address,payment_method, user_phone, user_allergy):
        # "create_user"함수를 이용해 우선 사용자를 DB에 저장
        user = self.create_user(
            login_id,
            password = password,
            user_nickname = user_nickname,
            current_address= current_address,
            payment_method=payment_method,
            user_phone=user_phone,
            user_allergy=user_allergy
        )
        # 관리자로 지정
        #user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    user_id = models.AutoField(primary_key=True)
    login_id = models.CharField(default='', max_length=45, null=False, blank=False, unique=True)
    
    #휴대폰번호 유효성 검사
    phoneNumberRegex = RegexValidator(regex = r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    user_phone = models.CharField(default='', max_length=11, null=False, blank=False, unique=True, validators = [phoneNumberRegex])
    
    current_address = models.CharField(default='', max_length=255, null=False, blank=False)
    payment_method = models.CharField(default='', max_length=255, null=False, blank=False)
    user_allergy = models.CharField(default='', max_length=255, blank=True, null=True)
    user_nickname = models.CharField(default='', max_length=45, unique=True, null=False, blank=False)
    #추가
    # login_password = models.CharField(default='', max_length=200, null=False)
    
    # email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
    # nickname = models.CharField(default='', max_length=100, null=False, blank=False, unique=True)
    # name = models.CharField(default='', max_length=100, null=False, blank=False)
    
    # User 모델의 필수 field
    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)
    
    # 출처: https://www.hides.kr/942 [Hide:티스토리]
    def get_full_name(self):        
        pass
    def get_short_name(self):
        pass
    @property    
    def is_superuser(self):        
        return self.is_admin    
        
    @property    
    def is_staff(self):       
        return self.is_admin    
    
    def has_perm(self, perm, obj=None):       
        return self.is_admin    
    
    def has_module_perms(self, app_label):       
        return self.is_admin    
        
    @is_staff.setter    
    def is_staff(self, value):        
        self._is_staff = value
    
    # 헬퍼 클래스 사용
    objects = UserManager()

    # 사용자의 username field는 nickname으로 설정
    USERNAME_FIELD = 'login_id'
    # PASSWORD_FIELD =  'login_passoword'
    # 필수로 작성해야하는 field
    REQUIRED_FIELDS = ['user_nickname', 'current_address', 'payment_method', 'user_phone', 'user_allergy']

    def __str__(self):
        return self.user_nickname

    #token을 만드는 함수
    @property
    def token(self):
        return self._generate_jwt_token( )

    # 토큰 발행 함수
    def _generate_jwt_token(self):
        dt = datetime.now( ) + timedelta(days=60) #60일 뒤에 토큰 완료됨
        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
            }, settings.SECRET_KEY, algorithm='HS256')
        return token