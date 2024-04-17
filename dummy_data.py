import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from faker import Faker
from account.models import Employee, Skills
import random


fake = Faker()
skills_tuple = (
    'Python',
    'Java',
    'JavaScript',
    'C++',
    'C#',
    'PHP',
    'Ruby',
    'Swift',
    'Kotlin',
    'Go',
    'HTML',
    'CSS',
    'SQL',
    'NoSQL',
    'React',
    'Angular',
    'Vue.js',
    'Django',
    'Flask',
    'Spring',
    'Node.js',
    'Express.js',
    'MongoDB',
    'PostgreSQL',
    'MySQL',
    'SQLite',
    'Firebase',
    'AWS',
    'Azure',
    'Docker',
    'Kubernetes',
    'Git',
    'Jenkins',
    'Ansible',
    'Terraform',
    'Linux',
    'Windows',
    'iOS',
    'Android',
    'Unity',
    'Unreal Engine'
    # Add more skills as needed
)
for skill_name in skills_tuple:
    skill, created = Skills.objects.get_or_create(name=skill_name)
    if created:
        print(f"Created skill: {skill_name}")
    else:
        print(f"Skill already exists: {skill_name}")
def genrate_employees(num):
    for _ in range(num):
        employee =  Employee.objects.create(
            nat_id = fake.unique.random_int(min=10000000000000, max=99999999999999), 
            first_name = fake.first_name(),
            last_name = fake.last_name(),
            email= fake.unique.email(),
            city = fake.city(),
            biography = fake.paragraph(),
            exp_level =  fake.random_element(elements=('Junior', 'Mid', 'Senior')) ,
            is_employer=False,
            password = "123"
        )
         # Generate a list of random skills for the employee
        num_skills = fake.random_int(min=1, max=50)  # Generate a random number of skills (between 1 and 5)
        employee_skills_names = fake.random_elements(elements=skills_tuple, unique=True, length=num_skills)
        employee_skills = [Skills.objects.get_or_create(name=name)[0] for name in employee_skills_names]
        # Assign the generated skills to the employee
        employee.skills.add(*employee_skills)
        employee.save()
genrate_employees(20)