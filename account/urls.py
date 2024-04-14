from django.urls import path 
from .views import *

urlpatterns = [
    path('register/employee', register, name='register_employee'),
    path('register/recruiter', register, name='register_recruiter'),
    path('login', my_login, name='my_login')
]