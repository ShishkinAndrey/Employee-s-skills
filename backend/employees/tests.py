from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
import random
from rest_framework.test import APIClient

from employees.factories import EmployeeFactory, EmployeeSkillFactory
from employees.models import Employee, EmployeeSkill
from employees.serializer import EmployeeSerializer, EmployeeSkillSerializer
from skills.factories import SkillFactory
from algorithms.factories import RequestSkillFactory, PresetFactory
from algorithms.serializer import PresetSerializer, RequestSkillSerializer
from algorithms.models import Preset, RequestSkill


class EmployeeCases(TestCase):
    @staticmethod
    def create_test_employee():
        EmployeeFactory()

    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_employees_list__auth_users_have_access(self):
        self.create_test_employee()
        emp = Employee.objects.all()
        serializer = EmployeeSerializer(emp, many=True)
        response = self.client.get(reverse('employees-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data'], serializer.data)

    def test_employees_list__guests_no_access(self):
        self.client.force_authenticate()
        self.create_test_employee()

        response = self.client.get(reverse('employees-list'))
        self.assertEqual(response.status_code, 401)

    def test_employees_retrieve__auth_users_have_access(self):
        self.create_test_employee()
        emp = Employee.objects.last()
        serializer = EmployeeSerializer(emp)
        response = self.client.get(reverse('employees-detail', kwargs={'pk': emp.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_employees_retrieve__guests_no_access(self):
        self.client.force_authenticate()
        self.create_test_employee()

        emp = Employee.objects.last()
        response = self.client.get(reverse('employees-detail', kwargs={'pk': emp.id}))
        self.assertEqual(response.status_code, 401)


class EmployeeSkillCases(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.employee = EmployeeFactory()
        self.skill = SkillFactory()

    def create_test_employee_skill(self):
        EmployeeSkillFactory(employee_id=self.employee, skill_id=self.skill)

    @staticmethod
    def row_response(response):
        return {'id': response['id'],
                'firstname': response['firstname'],
                'lastname': response['lastname'],
                'skills': response['skills']}

    def test_emp_skills_list__auth_users_have_access(self):
        self.create_test_employee_skill()
        response = self.client.get(reverse('emp_skills-list'))

        self.assertEqual(response.status_code, 200)
        for val in response.data['data']:
            self.assertEqual(val, self.row_response(val))

    def test_emp_skills_list__guests_no_access(self):
        self.client.force_authenticate()
        self.create_test_employee_skill()

        response = self.client.get(reverse('emp_skills-list'))
        self.assertEqual(response.status_code, 401)

    def test_emp_skills_retrieve__auth_users_have_access(self):
        self.create_test_employee_skill()
        response = self.client.get(reverse('emp_skills-detail', kwargs={'pk': self.employee.pk}), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.row_response(response.data))

    def test_emp_skills_retrieve__guests_no_access(self):
        self.client.force_authenticate()
        self.create_test_employee_skill()

        response = self.client.get(reverse('emp_skills-detail', kwargs={'pk': self.employee.pk}))
        self.assertEqual(response.status_code, 401)

    def test_method_post_emp_skills__auth_user(self):
        response = self.client.post(
            reverse('emp_skills_post',kwargs={'emp_id': self.employee.pk}),
            data={'data':[{"seniority_level": random.randint(1, 3),'skill_id': self.skill.pk}]},
            format='json')
        self.assertEquals(response.status_code, 201)

    def test_method_post_emp_skills__errors(self):
        self.client.force_authenticate()
        response = self.client.post(
            reverse('emp_skills_post',kwargs={'emp_id': self.employee.pk}),
            data={'data':[{"seniority_level": random.randint(1, 3),'skill_id': self.skill.pk}]},
            format='json')
        self.assertEquals(response.status_code, 401)

    def test_method_post_emp_skills__not_found(self):
        response = self.client.post(
            reverse('emp_skills_post', kwargs={'emp_id': self.employee.pk}),
            data={'data':[{"seniority_level": random.randint(1, 3), 'skill_id': 2}]},
            format='json')
        self.assertEquals(response.status_code, 404)

        response = self.client.post(
            reverse('emp_skills_post',kwargs={'emp_id': 2}),
            data={'data':[{"seniority_level": random.randint(1, 3),'skill_id': self.skill.pk}]},
            format='json')
        self.assertEquals(response.status_code, 404)

    def test_method_patch_emp_skills__auth_user(self):
        self.create_test_employee_skill()
        response = self.client.patch(
            reverse(
                'emp_skills_patch',
                kwargs={'emp_id': self.employee.pk, 'skill_id': self.skill.pk}
            ),
            data={"seniority_level": random.randint(1, 3)}, format='json')
        self.assertEquals(response.status_code, 200)

    def test_method_patch_emp_skills__errors(self):
        self.create_test_employee_skill()
        response = self.client.patch(
            reverse(
                'emp_skills_patch',
                kwargs={'emp_id': 2, 'skill_id': self.skill.pk}
            ),
            data={"seniority_level": random.randint(1, 3)}, format='json')
        self.assertEquals(response.status_code, 404)
        response = self.client.patch(
            reverse(
                'emp_skills_patch',
                kwargs={'emp_id': self.employee.pk, 'skill_id': 2}
            ),
            data={"seniority_level": random.randint(1, 3)}, format='json')
        self.assertEquals(response.status_code, 404)
        response = self.client.patch(
            reverse(
                'emp_skills_patch',
                kwargs={'emp_id': self.employee.pk, 'skill_id': self.skill.pk}
            ),
            data={"seniority_level": 4}, format='json')
        self.assertEquals(response.status_code, 400)
        response = self.client.patch(
            reverse(
                'emp_skills_patch',
                kwargs={'emp_id': self.employee.pk, 'skill_id': self.skill.pk}
            ),
            data={"seniority_level": str(random.randint(1, 3))}, format='json')
        self.assertEquals(response.status_code, 400)

    def test_method_delete_emp_skills__auth_user(self):
        self.create_test_employee_skill()
        response = self.client.delete(
            reverse(
                'emp_skills_delete',
                kwargs={'emp_id': self.employee.pk, 'skill_id': self.skill.pk}
            ))
        self.assertEquals(response.status_code, 200)

    def test_method_delete_emp_skills__errors(self):
        self.create_test_employee_skill()
        response = self.client.delete(
            reverse(
                'emp_skills_delete',
                kwargs={'emp_id': 2, 'skill_id': self.skill.pk}
            ))
        self.assertEquals(response.status_code, 404)
        response = self.client.delete(
            reverse(
                'emp_skills_delete',
                kwargs={'emp_id': self.employee.pk, 'skill_id': 2}
            ))
        self.assertEquals(response.status_code, 404)


class EmployeeSkillWeightCases(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.employee = EmployeeFactory()
        self.skill = SkillFactory()
        self.preset = PresetFactory()

    def create_test_employee_skill(self):
        EmployeeSkillFactory(employee_id=EmployeeFactory(), skill_id=self.skill)

    def create_request_skill(self):
        RequestSkillFactory(preset_id=self.preset, skill_id=self.skill)

    def test_method_post_weight__auth_user(self):
        for _ in range(2):
            self.create_test_employee_skill()

        response = self.client.post('get_employees_weight/',
                                    data={'data': [{"id": self.skill.pk,
                                                    "seniority": random.randint(1, 3),
                                                    "is_main": True}]},
                                    query_params={'algorithm_name': 'normalized'},
                                    format='json')

        self.assertEquals(response.status_code, 200)

    def test_method_post_weight_preset__auth_user(self):
        for _ in range(2):
            self.create_test_employee_skill()
        self.create_request_skill()

        response = self.client.post('/get_employees_weight_with_preset/self.preset.pk/',
                                    data={'data': [{"id": self.skill.pk,
                                                    "seniority": random.randint(1, 3),
                                                    "is_main": True}]},
                                    query_params={'algorithm_name': 'exponential'},
                                    format='json')
        self.assertEquals(response.status_code, 200)
