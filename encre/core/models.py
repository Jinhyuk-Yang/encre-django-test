from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

class UserManager(BaseUserManager):
    """Django가 제공하는 기본 User 관리자"""
    def create_user(self, email, password):
        """일반 계정 생성"""
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, password):
        """슈퍼 계정 생성"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """유저"""
    # 기본 정보
    email = models.EmailField(max_length=255, unique=True)

    # 사용자 인증 관련 (Default)
    is_superuser = models.BooleanField(default=False)
    login_ip = models.CharField(null=True, max_length=255)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    
    def save(self,*args, **kwargs):
        super(User, self).save(*args, **kwargs)

class Document(models.Model):
    """게시글"""
    head = models.CharField(max_length=64)
    body = models.CharField(max_length=1024)
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
