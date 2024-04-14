from django.forms import ModelForm
from .models import Employee, Profile
from django import forms

class EmployeeForm(ModelForm):
    """Reperesent the Employee class as a form
        for the registration page"""
    
    class Meta:
        model = Employee
        fields = ['nat_id', 'first_name', 'last_name', 'city', 'email', 'password', 'exp_level', 'biography']
        widgets = {
            'password': forms.PasswordInput,
            'biography': forms.Textarea(attrs= {'rows': 4})
        }
        labels = {
            'nat_id': "National ID"
        }
