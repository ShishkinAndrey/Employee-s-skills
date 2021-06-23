from django.db import models


class Competency(models.TextChoices):
    Python = 'Python', 'Python'
    Java = 'java', 'java'
    JavaScript = 'JavaScript', 'JavaScript'
    Databases = 'Databases', 'Databases'


class Skill(models.Model):
    skill = models.CharField(max_length=200)
    competency = models.CharField(max_length=200, choices=Competency.choices)

    def __str__(self):
        return self.skill

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'
