from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    EmployeesViewSet,
    EmployeeSkillViewSet,
    GetSkillWeightViewSet,
)

router = DefaultRouter()
router.register(r'get_employees', EmployeesViewSet, basename='employees')
router.register(r'get_employees_weight', GetSkillWeightViewSet, basename='employees_weight')


urlpatterns = [
    path('', include(router.urls)),
    path('get_employees_skills/', EmployeeSkillViewSet.as_view({'get': 'list'})),
    path('get_employee_skill/<int:pk>', EmployeeSkillViewSet.as_view({'get': 'retrieve'})),
    path('add_skills/<int:emp_id>', EmployeeSkillViewSet.as_view({'post': 'update'})),
    path('edit_skill/<int:emp_id>/<int:skill_id>', EmployeeSkillViewSet.as_view({'patch': 'partial_update'})),
    path('delete_skill/<int:emp_id>/<int:skill_id>', EmployeeSkillViewSet.as_view({'delete': 'destroy'})),
]
