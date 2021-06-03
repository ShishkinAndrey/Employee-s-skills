from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    employee_email = models.CharField(max_length=100)

    def __str__(self):
        return self.lastname

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employee'
