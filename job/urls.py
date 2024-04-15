from django.urls import path 
from .views import explore_jobs, post_jobs, job_details

urlpatterns = [
    path('', explore_jobs),
    path('job-posting', post_jobs, name='job-posting'),
    path('job-details/<int:id>/', job_details, name='job-details')
]