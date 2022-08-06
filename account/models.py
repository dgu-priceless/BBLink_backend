from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator 

# Create your models here.
class UserManager(BaseUserManager):
    # 일반 user 생성
    def create_user(self, login_id, user_nickname, user_phone, current_address, payment_method, user_allergy, login_password=None):
        print(login_id)
        if not login_id:
            raise ValueError('must have user login_id')
        if not user_nickname:
            raise ValueError('must have user nickname')
        if not user_phone:
            raise ValueError('must have user user_phone')
        if not current_address:
            raise ValueError('must have user current_address')
        if not payment_method:
            raise ValueError('must have user payment_method')

        user = self.model(
            login_id = login_id,
            user_nickname = user_nickname,
            user_phone = user_phone,
            current_address = current_address,
            payment_method = payment_method,
            user_allergy = user_allergy,
            #추가
            login_password = login_password
        )
        user.set_password(login_password)
        user.save(using=self._db)
        return user

    # 관리자 user 생성
    def create_superuser(self, login_id, user_nickname, login_password=None):
        user = self.create_user(
            login_id,
            login_password = login_password,
            user_nickname = user_nickname
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
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
    login_password = models.CharField(default='', max_length=200, null=False)

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
    USERNAME_FIELD = 'user_nickname'
    # 필수로 작성해야하는 field
    REQUIRED_FIELDS = ['login_id', 'user_phone']

    def __str__(self):
        return self.user_nickname