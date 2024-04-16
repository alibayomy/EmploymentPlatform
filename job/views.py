from django.shortcuts import render, redirect
from .forms import JobForm
from .models import Job, EmployeeJobs
from django.contrib.auth.decorators import login_required
from django import template
# Create your views here.



@login_required()
def post_jobs(request):

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            new_job = form.save(commit=False)
            new_job.employer = request.user
            new_job.save()
            form.save_m2m()
            return render(request, 'account/landing_page.html')
        else:
            context = {'form': form}
            return render (request, 'post_job.html', context)
    
    if request.user.is_authenticated and request.user.is_employer:
        form = JobForm()
        context = {'form': form}
        return render(request, 'post_job.html', context)
    return redirect("/")


@login_required()
def explore_jobs(request):
    """Get all the jobs out of database
        then render back to the employee"""
    jobs = Job.objects.all()
    context = {"jobs" :jobs}
    return render(request, 'explore_jobs.html', context)

@login_required()
def recommended_jobs(request):
    """Get the jobs that matches the 
        user Skills and biography"""
    user = request.user
    ## ==> code to be written here
    pass

@login_required()
def job_details(request, id):
    """Get the job details out of database based
        on the job_id"""

    job = Job.objects.get(id=id)
    context = {"job": job}
    return render(request, "job_details.html", context)

@login_required()
def apply_to_job(request):
    """Adding the job to the applied employee"""
    if request.method == 'POST':
        job = Job.objects.get(id=request.POST.get("job"))
        new_applied_job = EmployeeJobs.objects.create(employee=request.user, job=job)
        return redirect("/accounts/profile/")
    return redirect("/")


@login_required()
def get_employee_jobs(request):
    """Render a page that returns all
    the jobs the Employee applied for"""
    jobs = EmployeeJobs.objects.filter(employee_id = request.user.id) 
    context = {'jobs':jobs}
    return render(request, 'employee_jobs.html', context)