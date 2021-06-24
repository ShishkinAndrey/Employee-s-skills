from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from skills.factories import SkillFactory
from skills.models import Skill
from skills.serializer import SkillSerializer


class SkillCases(TestCase):
    @staticmethod
    def create_test_skill():
        SkillFactory()

    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_skills_list__auth_users_have_access(self):
        self.create_test_skill()
        skill = Skill.objects.all()
        serializer = SkillSerializer(skill, many=True)
        response = self.client.get(reverse('skills-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_skills_list__guests_no_access(self):
        self.client.force_authenticate()
        self.create_test_skill()

        response = self.client.get(reverse('skills-list'))
        self.assertEqual(response.status_code, 401)

    def test_skills_retrieve__auth_users_have_access(self):
        self.create_test_skill()
        skill = Skill.objects.last()
        serializer = SkillSerializer(skill)
        response = self.client.get(reverse('skills-detail', kwargs={'pk': skill.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_skills_retrieve__guests_no_access(self):
        self.client.force_authenticate()
        self.create_test_skill()

        skill = Skill.objects.last()
        response = self.client.get(reverse('skills-detail', kwargs={'pk': skill.id}))
        self.assertEqual(response.status_code, 401)
