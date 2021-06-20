from django.contrib import admin

from algorithms.models import Preset, RequestSkill


@admin.register(Preset)
class PresetAdmin(admin.ModelAdmin):

    fields = ('name', 'description')
    list_display = ('id', 'name', 'description')
    list_display_links = ('name', )
    search_fields = ('name',)

    class Meta:
        model = Preset


@admin.register(RequestSkill)
class RequestSkillAdmin(admin.ModelAdmin):

    fields = (('preset_id', 'skill_id'), ('is_main', 'seniority_level'))
    list_display = ('id', 'preset_id', 'skill_id', 'is_main', 'seniority_level')

    class Meta:
        model = RequestSkill
