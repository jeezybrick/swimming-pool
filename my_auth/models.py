from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from core.models import TimeStampedModel
from my_auth.managers import CustomUserManager


# Extend User model
class MyUser(AbstractUser, TimeStampedModel):

    USERNAME_FIELD = 'username'

    def __unicode__(self):
        return self.username

    class Meta(object):
        unique_together = ('email', )


class OAuthUser(AbstractBaseUser):

    fullname = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=30)
    email = models.EmailField(unique=False)
    is_auth = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return self.username

    def is_authenticated(self):
        return True

