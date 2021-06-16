from rest_framework.routers import DefaultRouter
from .views import (
    EmployeesViewSet,
    EmployeeSkillViewSet,
    GetSkillWeightViewSet,
)

router = DefaultRouter()
router.register(r'get_employees', EmployeesViewSet, basename='employees')
router.register(r'get_employees_skills', EmployeeSkillViewSet, basename='employees_skills')
router.register(r'get_employees_weight', GetSkillWeightViewSet, basename='employees_weight')
urlpatterns = router.urls