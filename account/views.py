from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Employee, Profile, ViewProfile
from .decorators import logout_required
from .forms import EmployeeForm, EmployerForm
from datetime import datetime
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
@logout_required()
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

@logout_required()
def my_login(request):
    """Rendring the login page for the user"""
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/accounts/profile/")
        else:
            return redirect("/accounts/login")
    else:
        form = EmployeeForm()
        context = {'form': form}
        return render(request, 'account/login.html', context=context)

def logout_view(request):
    """LogOut the curent from the system"""
    logout(request)
    return redirect("/")

@logout_required()
def homepage(request):
    """Rendring back the hompage of the project"""
    return render(request, 'landing/landing_page.html')

@login_required()
def user_profile(request):
    """Render the requested user profile
    """
    user = Profile.objects.get(employee_id=request.user.id)
    context = {'myuser':user}
    return render(request, 'account/profile.html', context)


def employee_profile(request, id):
    """Render the profesinal profile
        of the employees"""
    
    user = Employee.objects.get(id=id)
    profile = Profile.objects.get(employee=user)
    if request.user == user:
        profile_views = ViewProfile.objects.filter(profile=profile).count()
    else:
        profile_views = None
    if request.user.is_authenticated and request.user != user:
        #test if the employer viewed the profile before
        queries = ViewProfile.objects.filter(employer=request.user, profile=profile)
        if queries:
            for query in queries:
                query.viewed_on = datetime.now()
                query.save()
        else:
           ViewProfile.objects.create(employer=request.user, profile=profile)
           print("New view created")
           
    context = {'myuser':user, 'profile':profile, "views":profile_views}
    return render(request, 'account/employee_profile.html', context)