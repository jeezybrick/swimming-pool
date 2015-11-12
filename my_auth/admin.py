from django.contrib import admin
from my_auth.models import OAuthUser

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ("fullname", "email", 'is_auth', 'is_banned', 'banned_to')

admin.site.register(OAuthUser, UserAdmin)
