from django.db import models
from account.models import Employee, Skills
# Create your models here.




class Job(models.Model):
    """Job posted by the employer"""

    EXP_LEVEL = (
        ("Junior", "Junior"),
        ("Mid", "Mid"),
        ("Senior", "Senior")
    )
    employer = models.ForeignKey(Employee, on_delete=models.CASCADE)
    company = models.CharField(max_length=50, default="Intlaq")
    title = models.CharField(max_length=50)
    description = models.TextField()
    location = models.CharField(max_length=50)
    exp_level = models.CharField(max_length=6, choices=EXP_LEVEL)
    posted_on = models.DateField(auto_now_add=True)
    skills_required = models.ManyToManyField(Skills, related_name='Job_Skills')

class EmployeeJobs(models.Model):
    """Store the Jobs that each employee applied for"""
    STATUS = (
        ("Applied", "applied"),
        ("Not Selected", "not-selected"),
        ("Accepted", "accepted"),
        ("Viewed", "viewed")
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS, default="applied")
    applied_on = models.DateField(auto_now_add=True)

