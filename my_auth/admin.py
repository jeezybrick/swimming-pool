from django.contrib import admin
from my_auth.models import OAuthUser

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ("fullname", "username", "email", 'is_auth')

admin.site.register(OAuthUser, UserAdmin)
