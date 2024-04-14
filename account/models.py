from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Skills(models.Model):
    """Representing the programming language skills
    for each user"""
    name = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return self.name
    


def validate_nat_id(value):
    """Validate the national ID number for the employee
        raise an error if its length < 14"""
    try:
        int(value)
    except:
        raise ValidationError('National ID must consist of numbers only', params={'value':value})
    str_num = str(value)
    if len(str_num) < 14:
        raise ValidationError(('National ID  must be 14 number only'),params={'value':value})

class Employee(AbstractUser):
    """
    Represents the employee table in the database with attributes 
    Nat_id: primary key and the unique value
    """
    EXP_LEVEL = (
        ("J", "Junior"),
        ("M", "Mid"),
        ("S", "Senior")
    )
    nat_id = models.CharField(max_length=14, unique=True,
                                            validators=[validate_nat_id])
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=50)
    skills = models.ManyToManyField(to=Skills, related_name="employee_skills")
    biography = models.TextField()
    exp_level = models.CharField(max_length=6, choices=EXP_LEVEL)
    is_employer = models.BooleanField(default=False)
    username = models.CharField(max_length=150,null=True)

    #Overriding the authentication to email not username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nat_id', 'username']


    # def save(self, *args, **kwargs):
    #     """Hashing the password upong saving """
    #     if not self.is_superuser:
    #         self.set_password(self.password)
    #         super().save(*args, **kwargs)
    #     else:
    #         super().save(*args, **kwargs)

class Profile(models.Model):
    """Represent the profile of each user in 
        the system"""
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, upload_to='account/images', default='default.png')
    hits = models.IntegerField(default=0)

    def __str__(self) -> str:
        return (self.employee.email)


#Create a profile automatic when a new User register
def create_profile(sender, instance, created, **kwargs):
    """Create a profile and save for the new users"""
    print("The instance is ", instance)
    if created:
        user_profile = Profile(employee=instance)
        user_profile.save()

post_save.connect(create_profile, sender=Employee)