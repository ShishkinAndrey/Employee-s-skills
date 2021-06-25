from django.urls import path

from .views import (
    PresetViewSet,
)

urlpatterns = [
    path('get_presets/', PresetViewSet.as_view({'get': 'list'}), name='presets-list'),
    path('get_preset/<int:pk>', PresetViewSet.as_view({'get': 'retrieve'}), name='presets-retrieve'),
    path('add_preset', PresetViewSet.as_view({'post': 'create'}), name='add_preset'),
    path('add_skills/<int:preset_id>', PresetViewSet.as_view({'post': 'update'}), name='add_skills'),
    path('edit_skill/<int:preset_id>/<int:skill_id>', PresetViewSet.as_view({'patch': 'partial_update'}), name='edit_skills'),
    path('delete_preset/<int:preset_id>', PresetViewSet.as_view({'delete': 'destroy'}), name='delete_preset'),
    path('delete_skill/<int:preset_id>/<int:skill_id>', PresetViewSet.as_view({'delete': 'destroy_skill'}), name='delete_skill'),
]
