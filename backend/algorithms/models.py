from django.db import models

from skills.models import Skill


class Preset(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Preset'
        verbose_name_plural = 'Presets'


class RequestSkill(models.Model):
    preset_id = models.ForeignKey(Preset, verbose_name='preset', on_delete=models.CASCADE)
    skill_id = models.ForeignKey(Skill, verbose_name='skill', on_delete=models.PROTECT)
    is_main = models.BooleanField(null=False)
    seniority_level = models.IntegerField(null=False)

    class Meta:
        verbose_name = 'RequestSkill'
        verbose_name_plural = 'RequestSkill'