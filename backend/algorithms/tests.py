from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
import random
from rest_framework.test import APIClient

from algorithms.factories import PresetFactory, RequestSkillFactory
from algorithms.models import Preset, RequestSkill
from skills.factories import SkillFactory
from skills.models import Skill
from skills.serializer import SkillSerializer


class PresetCases(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.preset = PresetFactory()
        self.skill = SkillFactory()

    @staticmethod
    def create_test_preset():
        PresetFactory()

    def create_test_request_skill(self):
        RequestSkillFactory(preset_id=self.preset, skill_id=self.skill)

    @staticmethod
    def row_response(response):
        return {'id': response['id'],
                'name': response['name'],
                'description': response['description'],
                'skills': response['skills']}

    def test_preset_list__auth_users_have_access(self):
        self.create_test_request_skill()
        response = self.client.get(reverse('presets-list'))
        self.assertEqual(response.status_code, 200)
        for val in response.data['data']:
            self.assertEqual(val, self.row_response(val))

    def test_preset_list__guests_401(self):
        self.client.force_authenticate()
        self.create_test_request_skill()
        response = self.client.get(reverse('presets-list'))
        self.assertEqual(response.status_code, 401)

    def test_preset_retrieve__auth_users_have_access(self):
        self.create_test_request_skill()
        response = self.client.get(reverse('presets-retrieve', kwargs={'pk': self.preset.pk}), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.row_response(response.data))

    def test_preset_retrieve__guests_no_access(self):
        self.client.force_authenticate()
        self.create_test_request_skill()

        response = self.client.get(reverse('presets-retrieve', kwargs={'pk': self.preset.pk}))
        self.assertEqual(response.status_code, 401)

    def test_method_post_preset__auth_user_and_guest(self):
        data = {"name": "test_name",
                 "description": "test_description",
                 "skills": [{
                     "skill_id": self.skill.pk,
                     "seniority_level": 1,
                     "is_main": True}]}
        response = self.client.post(
            reverse('add_preset'),
            data=data,
            format='json')
        self.assertEquals(response.status_code, 201)

        self.client.force_authenticate()
        response = self.client.post(
            reverse('add_preset'),
            data=data,
            format='json')
        self.assertEquals(response.status_code, 401)

    def test_method_post_preset__404(self):
        sk = Skill.objects.all()
        ser = SkillSerializer(sk, many=True)
        print(ser.data)
        data = {"name": 'test_name',
                "description": 'test_description',
                "skills": [{"skill_id": 2,
                            "seniority_level": random.randint(1, 4),
                            "is_main": True}]}
        response = self.client.post(
            reverse('add_preset'),
            data=data,
            format='json')
        self.assertEquals(response.status_code, 404)

        data = {"name": "test_name",
                "description": "test_description",
                "skills": [{"skill_id": self.skill.pk,
                            "seniority_level": random.randint(4, 9),
                            "is_main": True}]}
        response = self.client.post(
            reverse('add_preset'),
            data=data,
            format='json')
        self.assertEquals(response.status_code, 400)

        data = {"name": "test_name",
                "description": "test_description",
                "skills": [{"skill_id": self.skill.pk,
                            "seniority_level": str(random.randint(1, 4)),
                            "is_main": True}]}
        response = self.client.post(
            reverse('add_preset'),
            data=data,
            format='json')
        self.assertEquals(response.status_code, 400)

    def test_method_post_add_skills_preset(self):
        self.create_test_preset()
        last_preset = Preset.objects.last()
        response = self.client.post(
            reverse('add_skills', kwargs={'preset_id': last_preset.pk}),
            data={'data': [{"skill_id": self.skill.pk, "seniority_level": random.randint(1, 4), "is_main": True}]},
            format='json')
        self.assertEquals(response.status_code, 200)

    def test_method_post_add_skills_preset_errors(self):
        response = self.client.post(
            reverse('add_skills', kwargs={'preset_id': 9999}),
            data={'data':[{"skill_id": self.skill.pk, "seniority_level": random.randint(1, 4), "is_main": False}]},
            format='json')
        self.assertEquals(response.status_code, 404)

        response = self.client.post(
            reverse('add_skills', kwargs={'preset_id': self.preset.pk}),
            data={'data': [{"skill_id": 99999, "seniority_level": random.randint(1, 4), "is_main": False}]},
            format='json')
        self.assertEquals(response.status_code, 404)

        response = self.client.post(
            reverse('add_skills', kwargs={'preset_id': self.preset.pk}),
            data={'data': [{"skill_id": self.skill.pk, "seniority_level": random.randint(4, 9), "is_main": False}]},
            format='json')
        self.assertEquals(response.status_code, 400)

    def test_method_patch_preset_skills(self):
        self.create_test_request_skill()
        response = self.client.patch(
            reverse(
                'edit_skills',
                kwargs={'preset_id': self.preset.pk, 'skill_id': self.skill.pk}
            ),
            data={"seniority_level": random.randint(1, 3)}, format='json')
        self.assertEquals(response.status_code, 200)

    def test_method_patch_preset_skills_errors(self):
        self.create_test_request_skill()
        response = self.client.patch(
            reverse(
                'edit_skills',
                kwargs={'preset_id': 2, 'skill_id': self.skill.pk}
            ),
            data={"seniority_level": random.randint(1, 3)}, format='json')
        self.assertEquals(response.status_code, 404)

        self.create_test_request_skill()
        response = self.client.patch(
            reverse(
                'edit_skills',
                kwargs={'preset_id': self.preset.pk, 'skill_id': 2}
            ),
            data={"seniority_level": random.randint(1, 3)}, format='json')
        self.assertEquals(response.status_code, 404)

    def test_method_delete_preset__auth_user(self):
        self.create_test_request_skill()
        response = self.client.delete(
            reverse(
                'delete_preset',
                kwargs={'preset_id': self.preset.pk}
            ))
        self.assertEquals(response.status_code, 200)

    def test_method_delete_emp_skills__auth_user(self):
        self.create_test_request_skill()
        response = self.client.delete(
            reverse(
                'delete_skill',
                kwargs={'preset_id': self.preset.pk, 'skill_id': self.skill.pk}
            ))
        self.assertEquals(response.status_code, 200)
