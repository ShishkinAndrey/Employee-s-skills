from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.shortcuts import get_object_or_404
from rest_framework.test import APIClient

from employees.factories import EmployeeFactory, EmployeeSkillFactory
from employees.models import Employee, EmployeeSkill
from employees.serializer import EmployeeSerializer
from skills.factories import SkillFactory


# class EmployeeCases(TestCase):
#     @staticmethod
#     def create_test_employee():
#         EmployeeFactory()
#
#     def setUp(self):
#         self.user = get_user_model().objects.create(username='test_user', password='password')
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)
#
#     def test_employees_list__auth_users_have_access(self):
#         self.create_test_employee()
#         emp = Employee.objects.all()
#         serializer = EmployeeSerializer(emp, many=True)
#         response = self.client.get(reverse('employees-list'))
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data['data'], serializer.data)
#
#     def test_employees_list__guests_no_access(self):
#         self.client.force_authenticate()
#         self.create_test_employee()
#
#         response = self.client.get(reverse('employees-list'))
#         self.assertEqual(response.status_code, 401)
#
#     def test_employees_retrieve__auth_users_have_access(self):
#         self.create_test_employee()
#         emp = Employee.objects.last()
#         serializer = EmployeeSerializer(emp)
#         response = self.client.get(reverse('employees-detail', kwargs={'pk': emp.id}))
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data, serializer.data)
#
#     def test_employees_retrieve__guests_no_access(self):
#         self.client.force_authenticate()
#         self.create_test_employee()
#
#         emp = Employee.objects.last()
#         response = self.client.get(reverse('employees-detail', kwargs={'pk': emp.id}))
#         self.assertEqual(response.status_code, 401)


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
        employees_list = []
        # get_employees = Employee.objects.all().values('id', 'firstname', 'lastname')
        #
        # for row in get_employees:
        #     result = row
        #     get_employees_skills = EmployeeSkill.objects \
        #         .filter(employee_id=row['id']) \
        #         .values('seniority_level',
        #                 'skill_id'
        #                 )
        #     if get_employees_skills:
        #         result['skills'] = get_employees_skills
        #     employees_list.append(result)
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
        # queryset = Employee.objects.all().values('id', 'firstname', 'lastname')
        # get_employee = get_object_or_404(queryset, pk=self.employee.pk)
        # get_employee_skills = EmployeeSkill.objects.filter(employee_id=self.employee.pk).values('seniority_level',
        #                                                                           'skill_id')
        # emp_dict = {
        #     'employee_id': get_employee['id'],
        #     'firstname': get_employee['firstname'],
        #     'lastname': get_employee['lastname'],
        #     'skills': get_employee_skills,
        # }
        response = self.client.get(reverse('emp_skills-detail', kwargs={'pk': self.employee.pk}), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.row_response(response.data))

    def test_emp_skills_retrieve__guests_no_access(self):
        self.client.force_authenticate()
        self.create_test_employee_skill()

        response = self.client.get(reverse('emp_skills-detail', kwargs={'pk': self.employee.pk}))
        self.assertEqual(response.status_code, 401)

