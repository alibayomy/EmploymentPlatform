from django.forms import ModelForm
from .models import Employee, Profile


class EmployeeForm(ModelForm):
    """Reperesent the Employee class as a form
        for the registration page"""

    class Meta:
        model = Employee
        fields = ('email'),