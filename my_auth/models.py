from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from core.models import TimeStampedModel
from my_auth.managers import CustomUserManager
from django.contrib.auth.models import UserManager


class OAuthUser(AbstractBaseUser, PermissionsMixin):

    fullname = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    kind = models.CharField(max_length=1000)
    member_id = models.CharField(max_length=50, default='')
    banned_to = models.DateTimeField(null=True)
    attempt_to_ban = models.IntegerField(default=0)
    is_auth = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return self.username

    def is_authenticated(self):
        return True

    def get_short_name(self):
        "Returns the short name for the user."
        return self.fullname


