from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/employees/', include('employees.urls')),
    url(r'^api/skills/', include('skills.urls')),

]

