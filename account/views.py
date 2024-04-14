from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, get_user_model
from .models import Employee, Profile
from .forms import EmployeeForm
User = get_user_model()
# Create your views here.
print(User)

def register(request):
    """Rendring the register view to 
        handel the input data"""
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            print(form.errors)
            return redirect('/')
        else:
            context = {'form': form}
            return render(request, 'account/register.html', context=context)

    form = EmployeeForm()
    context = {'form': form}
    return render(request, 'account/register.html', context=context)



def my_login(request):
    """Rendring the login page for the user"""
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        print(authenticate(request, email=email, password=password))
        print(f"Email is {email} & Password {password}")
        if user is not None:
            login(request, user)
            return redirect("landing/landing_page.html")
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