from django.urls import path 
from .views import *

urlpatterns = [
    path('', explore_jobs),
    path('job-posting', post_jobs, name='job-posting'),
    path('job-details/<int:id>/', job_details, name='job-details'),
    path('job-apply/', apply_to_job, name='apply-to-job' ),
    path('employee-jobs/', get_employee_jobs)
]