from django.contrib import admin
from django.db import models

from skills.models import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):

    fields = ('skill', 'competency', )
    list_display = ('id', 'skill', 'competency')
    list_display_links = ('skill', )
    search_fields = ('skill', )

    class Meta:
        model = Skill
