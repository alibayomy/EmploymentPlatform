from django.shortcuts import render
from .models import Employee, Profile
from .forms import EmployeeForm
# Create your views here.


def register(request):
    form = EmployeeForm()
    context = {'form': form}
    return render(request, 'account/register.html', context=context)
