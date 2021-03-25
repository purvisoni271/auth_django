from django.contrib import admin
from auth_rest_app.models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')

admin.site.register(User, UserAdmin)
