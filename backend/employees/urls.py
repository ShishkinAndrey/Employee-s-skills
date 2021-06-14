from rest_framework.routers import DefaultRouter
from django.urls import path

from . import views
from .views import EmployeesViewSet

router = DefaultRouter()
router.register(r'get_employees', EmployeesViewSet, basename='employees')
# router.register(r'get_employees_skills', EmployeesSkillsViewSet, basename='employees_skills')

# urlpatterns = [
#     path('/get_employees/', views.EmployeesViewSet.as_view()),
#     path('/get_employees/<int:pk>/', views.DetailedEmployeesViewSet.as_view()),
#
# ]
urlpatterns = router.urls
