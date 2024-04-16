from django.urls import path 
from .views import *

urlpatterns = [
    path('register/employee', register, name='register_employee'),
    path('register/employer', employer_register, name='register_employer'),
    path('login/', my_login, name='my_login'),
    path('logout/', logout_view, name='my_logout'),
    path('profile/', user_profile, name='profile'),
    path('employee-profile/<int:id>/', employee_profile, name='employee-profile')
]