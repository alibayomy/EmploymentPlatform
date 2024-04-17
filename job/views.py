from itertools import chain
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Count, Subquery ,Q
from account.models import Skills, Employee, Profile
from .models import Job, EmployeeJobs
from .forms import JobForm
from django import template
from datetime import datetime
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
    if not request.user.is_employer:
        jobs = Job.objects.all()
        context = {"jobs" :jobs}
        return render(request, 'explore_jobs.html', context)
    return render(request, 'error_page.html')


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

        if request.method == 'POST':
            employee_id = request.POST['employee']
            application = EmployeeJobs.objects.get(job=job, employee_id=employee_id)

            if request.POST['button'] == 'accepted':
                application.status = "accepted"
                application.save()

            else:
                application.status = "not-selected"
                application.save()
            return redirect('/accounts/profile/')
        else:
            #Method = GET
           
           
            emp_job = EmployeeJobs.objects.filter(job_id=job_id)
            job_skills = job.skills_required.all()
            job_skills_lst = []
            for skill in job_skills:
                job_skills_lst.append(str(skill))
            print(job_skills_lst)
            job_location = job.location.split()
            employees = Employee.objects.filter(id__in=emp_job.values("employee_id"))
            filter_values = {'All': employees,
                             'Skills':employees.filter(skills__in=job_skills).distinct() , 
                             'City':employees.filter(city__in=job_location).distinct(), 
                             'Exp':employees.filter(exp_level__in=job.exp_level).distinct(), 
                             'Bio':0}
            
            search_param = request.GET.get('filter')
            if(search_param == 'Bio'):
                matched_emp_ids = []
                for employee in employees:
                # Check which part of the biography matched
                    for skill in job_skills_lst:
                        if employee.biography.__contains__(skill):
                            matched_emp_ids.append(employee.id)
                employees = Employee.objects.filter(id__in=matched_emp_ids)
                print(employees)
            else:
                for key, value in filter_values.items():
                    if (search_param == key):
                        employees= value
                        break
                else:
                    pass
            
            for employee in employees:
                employee.applied_date = EmployeeJobs.objects.filter(employee=employee, job_id=job_id).values("applied_on").first()['applied_on']
                employee.application_status = EmployeeJobs.objects.filter(employee=employee, job_id=job_id).values("status").first()['status']
                
            context = {'employees':employees, 'job': job, 'search_param':search_param, 'filter_values':filter_values}
            return render(request, 'job_applications.html', context)
    else:
        return render(request, 'error_page.html')
        

@login_required()
def filter_job_applications(request, query):
    """Filter the job applications based on 
        the given filter query"""
    pass


@login_required()
def search_view(request):

    search_query = request.GET.get('search')
    if request.user.is_employer:
        employees = Employee.objects.filter(is_employer=False).filter(Q(first_name__contains=search_query) | Q(last_name__contains=search_query) | Q(email__contains=search_query))
        profiles = Profile.objects.filter(employee__in=employees)
        context = {"profiles" : profiles}
        return render(request, 'employer_search_page.html', context=context)

    else:
        jobs = Job.objects.filter(Q(company__contains=search_query))
        context = {"jobs":jobs}
        return render(request, 'employee_search_page.html', context=context)


@login_required()
def get_employees_profiles(request):
    """Render all the profiles for the employer"""

    if request.user.is_employer:
        profiles = Profile.objects.filter(employee__is_employer = False)
        for profile in profiles:
            print(profile.employee.first_name)
        context = {"profiles": profiles}
    return render(request, 'employer_profiles.html', context=context)