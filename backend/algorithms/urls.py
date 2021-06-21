from django.urls import path

from .views import (
    PresetViewSet,
)

urlpatterns = [
    path('get_presets/', PresetViewSet.as_view({'get': 'list'})),
    path('get_preset/<int:pk>', PresetViewSet.as_view({'get': 'retrieve'})),
    path('add_preset', PresetViewSet.as_view({'post': 'create'})),
    path('add_skills/<int:preset_id>', PresetViewSet.as_view({'post': 'update'})),
    path('edit_skill/<int:preset_id>/<int:skill_id>', PresetViewSet.as_view({'patch': 'partial_update'})),
    path('delete_preset/<int:preset_id>', PresetViewSet.as_view({'delete': 'destroy'})),
    path('delete_skill/<int:preset_id>/<int:skill_id>', PresetViewSet.as_view({'delete': 'destroy_skill'})),
]
