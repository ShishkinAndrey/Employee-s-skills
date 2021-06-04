from rest_framework.routers import DefaultRouter

from skills.views import SkillViewSet

router = DefaultRouter()
router.register(r'', SkillViewSet, basename='employees')

urlpatterns = router.urls
