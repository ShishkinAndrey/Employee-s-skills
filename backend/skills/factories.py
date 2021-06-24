import factory
from faker import Faker

from skills.models import Skill

fake = Faker()


class SkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Skill

    skill = factory.LazyAttribute(lambda _: fake.word())
    competency = factory.LazyAttribute(lambda _: fake.word())
