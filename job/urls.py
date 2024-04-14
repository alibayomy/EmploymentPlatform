from django.urls import path 
from .views import explore_jobs, post_jobs

urlpatterns = [
    path('', explore_jobs),
    path('job-posting', post_jobs, name='job-posting')
]