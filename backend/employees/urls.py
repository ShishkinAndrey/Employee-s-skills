from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    EmployeesViewSet,
    EmployeeSkillViewSet,
    GetSkillWeightViewSet,
)


urlpatterns = format_suffix_patterns(
    [
        path('get_employees/', EmployeesViewSet.as_view({'get': 'list'})),
        path('get_employees/<int:pk>/', EmployeesViewSet.as_view({'get': 'retrieve'})),

        path('get_employees_skills/', EmployeeSkillViewSet.as_view({'get': 'list'})),
        path('get_employees_skills/<int:pk>/', EmployeeSkillViewSet.as_view({'get': 'retrieve'})),

        path('get_employees_weight/', GetSkillWeightViewSet.as_view({'put': 'update'})),
    ]
)