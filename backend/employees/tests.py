from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from employees.factories import EmployeeFactory
from employees.models import Employee, EmployeeSkill
from employees.serializer import EmployeeSerializer


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
