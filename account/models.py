from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
# Create your models here.

def validate_nat_id(value):
    """Validate the national ID number for the employee
        raise an error if its length < 14"""
    str_num = str(value)
    if len(str_num < 14):
        raise ValidationError((f'{value} must be 14 number only'),params={'value':value})

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
    nat_id = models.CharField(max_length=14, primary_key=True, unique=True, 
                                            validators=[validate_nat_id])
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=50)
    biography = models.TextField()
    exp_level = models.CharField(max_length=6, choices=EXP_LEVEL)

    #Overriding the authentication to email not username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Profile(models.Model):
    """Represent the profile of each user in 
        the system"""
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, upload_to='account/images', default='default.png')
    hits = models.IntegerField(default=0)

    def __str__(self) -> str:
        return (self.employee.email)
    
