from django.contrib import admin

from employees.models import Employee, EmployeeSkill


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    fields = (('firstname', 'lastname'), 'employee_email')
    list_display = ('firstname', 'lastname', 'employee_email')
    list_display_links = ('lastname', )
    search_fields = ('firstname', 'lastname', )

    class Meta:
        model = Employee


@admin.register(EmployeeSkill)
class EmployeeSkillAdmin(admin.ModelAdmin):

    fields = ('employee_id', 'skill_id', 'seniority_level')
    list_display = ('employee_id', 'skill_id', 'seniority_level')
    search_fields = ('employee_id',)

    class Meta:
        model = EmployeeSkill
