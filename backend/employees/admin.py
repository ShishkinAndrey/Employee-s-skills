from django.contrib import admin
from django.db import models

from employees.models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    fields = (('firstname', 'lastname'), 'employee_email')
    list_display = ('firstname', 'lastname', 'employee_email')
    list_display_links = ('lastname', )
    search_fields = ('firstname', 'lastname', )

    class Meta:
        model = Employee
