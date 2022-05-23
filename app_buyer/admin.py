from django.contrib import admin
from app_buyer.models import User
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display= ['fullname', 'email', 'password']