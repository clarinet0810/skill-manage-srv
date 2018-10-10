from django.contrib import admin
from .models import User, UserToken

admin.site.register(User)

class UserTokenAdmin(admin.ModelAdmin):
    fields = ['user', 'token', 'access_datetime',]

admin.site.register(UserToken, UserTokenAdmin)