import re
from django.db import models
from django.core import validators
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
    
        #Create user
        user = self.model(username=username, email=email, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, username, password, email=None, **extra_fields):
        user = self._create_user(username=username, email=email, password=password,
                                 is_staff=True, is_superuser=True)
        
        user.is_active = True
        user.save(using=self._db)
        return user
    
    
    def create_user(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, False, False,**extra_fields)
    

class User(AbstractBaseUser): 
    #atributes
    username = models.CharField(_('username'), max_length=15, null=False, unique=True)
    first_name = models.CharField(_('first name'), max_length=15, null=False)
    last_name = models.CharField(_('last name'), max_length=50, null=False)
    email = models.EmailField(_('email'), max_length=200, null= False, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_superuser = models.BooleanField(_('status User'), default=False)


    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    
    objects = UserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    #methods
    def __str__(self):
        return f"{self.email}"
    
    def get_short_name(self):
        return f"{self.first_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    




# Create your models here.
