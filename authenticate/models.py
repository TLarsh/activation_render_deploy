import random
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have an email')
        
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user
        
        
    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')
        
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=225, unique=True, db_index=True)
    email = models.EmailField(max_length=225, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    account_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    def save(self, *args, **kwargs):
        if not self.account_number:
            generator = str(random.randint(1000000000, 9999999999))
            self.account_number = f'013{generator}'[0:10]
        super().save(*args, **kwargs)
        
    def deposite(self, amount):
        self.balance += amount
        self.save()
        
    def transfer(self, account_number, amount):
        recipient = User.objects.get(account_number=account_number)
        if self.balance >= amount:
            self.balance -= amount 
            recipient.balance += amount
            self.save()
            recipient.save()
        else:
            raise ValueError("Insufficient balance to transfer")

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }