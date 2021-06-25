import random
import factory
from faker import Faker

from employees.models import Employee, EmployeeSkill

fake = Faker()


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    employee_email = factory.LazyAttribute(lambda _: '%s@example.com')
    firstname = factory.Faker('first_name')
    lastname = factory.Faker('last_name')


class EmployeeSkillFactory(factory.django.DjangoModelFactory):
    def __init__(self,  employee_id, skill_id):
        self.employee_id = employee_id
        self.skill_id = skill_id

    class Meta:
        model = EmployeeSkill

    seniority_level = random.randint(1, 3)
