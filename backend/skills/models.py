from django.db import models


class Skill(models.Model):
    COMPETENCY = (
        (1, 'python'),
        (2, 'java'),
        (3, 'js'),
        (4, '.net'),
    )
    skill = models.CharField(max_length=200)
    competency = models.CharField(max_length=200, choices=COMPETENCY)

    def __str__(self):
        return self.skill

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'
