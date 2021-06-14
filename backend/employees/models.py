from django.db import models

from skills.models import Skill


class Employee(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    employee_email = models.EmailField()

    def __str__(self):
        return self.lastname

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employee'


class EmployeeSkill(models.Model):
    employee_id = models.ForeignKey(Employee, verbose_name='employee', on_delete=models.PROTECT)
    skill_id = models.ForeignKey(Skill, verbose_name='skill', on_delete=models.PROTECT)
    seniority_level = models.IntegerField()

    class Meta:
        verbose_name = 'EmployeeSkill'
        verbose_name_plural = 'EmployeeSkills'


