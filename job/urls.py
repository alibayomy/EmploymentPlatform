from django.urls import path 
from .views import *

urlpatterns = [
    path('', explore_jobs),
    path('profiles/', get_employees_profiles),
    path('recommended/', recommended_jobs),
    path('job-posting', post_jobs, name='job-posting'),
    path('job-details/<int:job_id>/', job_details, name='job-details'),
    path('job-apply/', apply_to_job, name='apply-to-job' ),
    path('employee-jobs/', get_employee_jobs),
    path('job-applications/<int:job_id>/', get_job_applications, name='job-applications'),
    path('search/', search_view, name='search-page')
]