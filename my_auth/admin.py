from django.contrib import admin
from my_auth.models import MyUser

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "created_at", 'updated')

admin.site.register(MyUser, UserAdmin)
