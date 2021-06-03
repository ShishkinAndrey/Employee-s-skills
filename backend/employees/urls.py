from rest_framework.routers import DefaultRouter

from employees.views import EmployeesViewSet

router = DefaultRouter()
router.register(r'', EmployeesViewSet, basename='employees')

urlpatterns = router.urls
