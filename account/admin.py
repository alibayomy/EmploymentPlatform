from django.contrib import admin
from .models import Employee, Profile
from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.register(Employee)
