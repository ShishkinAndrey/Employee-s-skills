from rest_framework.routers import DefaultRouter
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .views import EmployeesViewSet, EmployeeSkillViewSet

# router = DefaultRouter()
# router.register(r'get_employees', EmployeesViewSet, basename='employees')
# # router.register(r'get_employees_skills', EmployeesSkillsViewSet, basename='employees_skills')
# urlpatterns = router.urls

# urlpatterns = [
#     path('get_employees/', views.EmployeesViewSet.as_view()),
#     path('get_employees/<int:pk>/', views.DetailedEmployeesViewSet.as_view()),
#
# ]

urlpatterns = format_suffix_patterns(
    [
        path('get_employees/', EmployeesViewSet.as_view({'get': 'list'})),
        path('get_employee/<int:pk>/', EmployeesViewSet.as_view({'get': 'retrieve'})),

        path('get_employees_skills/', EmployeeSkillViewSet.as_view({'get': 'list'})),
        path('get_employees_skills/<int:pk>/', EmployeeSkillViewSet.as_view({'get': 'retrieve'})),
    ]
)