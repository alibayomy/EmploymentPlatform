from django.urls import path 
from .views import *

urlpatterns = [
    path('register/employee', register, name='register_employee'),
    path('register/employer', employer_register, name='register_employer'),
    path('login/', my_login, name='my_login')
]