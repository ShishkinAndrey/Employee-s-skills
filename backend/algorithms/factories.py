import random
import factory
from faker import Faker

from algorithms.models import Preset, RequestSkill

fake = Faker()


class PresetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Preset

    name = factory.LazyAttribute(lambda _: fake.word())
    description = factory.LazyAttribute(lambda _: fake.word())


class RequestSkillFactory(factory.django.DjangoModelFactory):
    def __init__(self,  preset_id, skill_id):
        self.preset = preset_id
        self.skill_id = skill_id

    class Meta:
        model = RequestSkill

    seniority_level = random.randint(1, 3)
    is_main = True
