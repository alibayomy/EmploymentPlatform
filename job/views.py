from itertools import chain
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Count
from account.models import Skills, Employee
from .models import Job, EmployeeJobs
from .forms import JobForm
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
    user_skills= user.skills.all()
    bio = user.biography.split()
    user_skills_bio = Skills.objects.filter(name__in=bio)
    user_skills_all = chain(user_skills, user_skills_bio)
    jobs_related_by_skills = Job.objects.filter(skills_required__in=user_skills_all).distinct()

    context={'jobs':jobs_related_by_skills}
    return render(request, 'recommended_jobs.html', context)

@login_required()
def job_details(request, job_id):
    """Get the job details out of database based
        on the job_id"""

    try:
        EmployeeJobs.objects.get(job_id=job_id, employee_id=request.user.id)
        flag = 1
    except:
        flag=0
    
    job = Job.objects.get(id=job_id)
    context = {"job": job, 'flag':flag}
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
    if (request.user.is_employer):
        jobs = Job.objects.filter(employer_id= request.user.id).annotate(application_number=Count("employeejobs"))           
        context = {'jobs': jobs}
        return render(request, 'employer_jobs.html', context)
    else:
        jobs = EmployeeJobs.objects.filter(employee_id = request.user.id) 
        context = {'jobs':jobs}
    return render(request, 'employee_jobs.html', context)

@login_required()
def get_job_applications(request, job_id):
    """Render back all the job applications"""

    job = Job.objects.get(id=job_id)
    if request.user == job.employer:
        emp_job = EmployeeJobs.objects.filter(job_id=job_id)
        employee = Employee.objects.filter(id__in=emp_job.values("employee_id"))
        context = {'employees':employee}
        return render(request, 'job_applications.html', context)