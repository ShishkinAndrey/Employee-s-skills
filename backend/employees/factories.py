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
