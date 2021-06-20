from django.urls import path

from .views import (
    PresetViewSet,
)

urlpatterns = [
    path('get_presets/', PresetViewSet.as_view({'get': 'list'})),
    path('get_preset/<int:pk>', PresetViewSet.as_view({'get': 'retrieve'})),
    path('add_preset', PresetViewSet.as_view({'post': 'create'})),
    # path('edit_skill/<int:emp_id>/<int:skill_id>', EmployeeSkillViewSet.as_view({'patch': 'partial_update'})),
    # path('delete_skill/<int:emp_id>/<int:skill_id>', EmployeeSkillViewSet.as_view({'delete': 'destroy'})),
]
