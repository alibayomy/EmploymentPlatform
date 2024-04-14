from django.shortcuts import render, redirect
from .forms import JobForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def explore_jobs(request):
    return render(request, 'explore_jobs.html')

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