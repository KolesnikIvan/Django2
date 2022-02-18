from datetime import timedelta
from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.timezone import now


def get_activation_key_expiration_date():
    return now() + timedelta(hours=48)

# Create your models here.
# class ShopUser(AbstractBaseUser):  # models.Model):
class ShopUser(AbstractUser):  # models.Model):
    username = models.CharField(verbose_name='name', default='default user', unique=True, max_length=20)
    age = models.PositiveIntegerField(verbose_name='age')
    avatar = models.ImageField(verbose_name='avatar', blank=True, upload_to='users')
    phone = models.CharField(verbose_name='telephone', max_length=20, blank=True)  # , unique=True)
    city = models.CharField(verbose_name='city', max_length=20, blank=True)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=get_activation_key_expiration_date())
    
    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True
            