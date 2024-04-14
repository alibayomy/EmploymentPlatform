from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, get_user_model
from .models import Employee, Profile
from .forms import EmployeeForm, EmployerForm
User = get_user_model()
# Create your views here.


def register(request):
    """Rendring the register view to 
        handel the input data"""
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            new_employee = form.save()
            new_employee.set_password(form.cleaned_data["password"]) #=> Hashing the password for the user
            new_employee.save()
            return redirect('/accounts/login/')
        else:
            context = {'form': form}
            return render(request, 'account/register.html', context=context)

    form = EmployeeForm()
    context = {'form': form}
    return render(request, 'account/register.html', context=context)

def employer_register(request):
    """Rendring the register view to 
        handel the input data"""
    if request.method == 'POST':
        form = EmployerForm(request.POST)
        if form.is_valid():
            new_employer = form.save()
            new_employer.set_password(form.cleaned_data["password"]) #=> Hashing the password for the user
            new_employer.is_employer = True
            new_employer.save()
            return redirect('/accounts/login/')
        else:
            context = {'form': form}
            return render(request, 'account/employer_register.html', context=context)

    form = EmployerForm()
    context = {'form': form}
    return render(request, 'account/employer_register.html', context=context)


def my_login(request):
    """Rendring the login page for the user"""
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            print("Invalid User")
            return redirect("/accounts/login")
    else:
        form = EmployeeForm()
        context = {'form': form}
        return render(request, 'account/login.html', context=context)

def homepage(request):
    """Rendring back the hompage of the project"""
    return render(request, 'landing/landing_page.html')