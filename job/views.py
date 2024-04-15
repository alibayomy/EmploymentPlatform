from django.shortcuts import render, redirect
from .forms import JobForm
from .models import Job
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

def explore_jobs(request):
    """Get all the jobs out of database
        then render back to the employee"""
    jobs = Job.objects.all()
    context = {"jobs" :jobs}
    return render(request, 'explore_jobs.html', context)


def recommended_jobs(request):
    """Get the jobs that matches the 
        user Skills and biography"""
    user = request.user
    ## ==> code to be written here
    pass


def job_details(request, id):
    """Get the job details out of database based
        on the job_id"""

    job = Job.objects.get(id=id)
    context = {"job": job}
    return render(request, "job_details.html", context)


