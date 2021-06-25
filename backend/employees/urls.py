from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    EmployeesViewSet,
    EmployeeSkillViewSet,
    GetSkillWeightViewSet,
    PresetGetSkillWeightViewSet,
)

router = DefaultRouter()
router.register(r'get_employees', EmployeesViewSet, basename='employees')

urlpatterns = [
    path('', include(router.urls)),
    path('get_employees_skills/', EmployeeSkillViewSet.as_view({'get': 'list'}), name='emp_skills-list'),
    path('get_employee_skill/<int:pk>', EmployeeSkillViewSet.as_view({'get': 'retrieve'}), name='emp_skills-detail'),
    path('add_skills/<int:emp_id>', EmployeeSkillViewSet.as_view({'post': 'update'}), name='emp_skills_post'),
    path('edit_skill/<int:emp_id>/<int:skill_id>', EmployeeSkillViewSet.as_view({'patch': 'partial_update'}), name='emp_skills_patch'),
    path('delete_skill/<int:emp_id>/<int:skill_id>', EmployeeSkillViewSet.as_view({'delete': 'destroy'}), name='emp_skills_delete'),
    path('get_employees_weight', GetSkillWeightViewSet.as_view({'post': 'create'}), name='emp_weight'),
    path('get_employees_weight_with_preset/<int:pk>', PresetGetSkillWeightViewSet.as_view({'post': 'create'}), name='emp_weight_preset'),
]
