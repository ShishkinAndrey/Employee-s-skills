from django.urls import path

from .views import (
    PresetViewSet,
)

urlpatterns = [
    path('get_presets/', PresetViewSet.as_view({'get': 'list'})),
    # path('get_employee_skill/<int:pk>', EmployeeSkillViewSet.as_view({'get': 'retrieve'})),
    # path('add_skills/<int:emp_id>', EmployeeSkillViewSet.as_view({'post': 'update'})),
    # path('edit_skill/<int:emp_id>/<int:skill_id>', EmployeeSkillViewSet.as_view({'patch': 'partial_update'})),
    # path('delete_skill/<int:emp_id>/<int:skill_id>', EmployeeSkillViewSet.as_view({'delete': 'destroy'})),
]
