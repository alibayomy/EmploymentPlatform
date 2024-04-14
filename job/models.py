from django.db import models
from account.models import Employee, Skills
# Create your models here.




class Job(models.Model):
    """Job posted by the employer"""

    EXP_LEVEL = (
        ("J", "Junior"),
        ("M", "Mid"),
        ("S", "Senior")
    )
    employer = models.ForeignKey(Employee, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    location = models.CharField(max_length=50)
    exp_level = models.CharField(max_length=6, choices=EXP_LEVEL)
    posted_on = models.DateField(auto_now_add=True)
    skills_required = models.ManyToManyField(Skills, related_name='Job_Skills')

