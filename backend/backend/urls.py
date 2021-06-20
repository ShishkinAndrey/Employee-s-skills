from django.conf import settings
from django.conf.urls import url

from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Graduation Project API",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/skills/', include('skills.urls')),
    url(r'^api/employees/', include('employees.urls')),
    url(r'^api/presets/', include('algorithms.urls')),
    url(r'^api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

