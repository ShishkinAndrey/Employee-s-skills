from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from employees.models import Employee, EmployeeSkill
from employees.serializer import EmployeeSerializer, EmployeeSkillSerializer
from algorithms.algorithms import exponential_weight_algorithm

response_schema_dict = {
    "200": openapi.Response(
        description="200: Successfully read list of employees",
        examples={
            "application/json": {
                "firstname": "string",
                "lastname": "string",
                "employee_email": "string"
            }
        }
    ),
}

class EmployeesViewSet(viewsets.ViewSet):
    # @swagger_auto_schema(responses=response_schema_dict)
    def list(self, request):
        """ Read all
            ---
            get:
              operationId: current_app.categories.read_all_category
              tags:
                - Categories
              summary: Get list of categories
              description: Get list of categories
        """
        queryset = Employee.objects.all()
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Employee.objects.all()
        employee = get_object_or_404(queryset, pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)


class EmployeeSkillViewSet(viewsets.ViewSet):
    def list(self, request):
        employees_list = []
        get_employees = Employee.objects.all()
        serializer_employee = EmployeeSerializer(get_employees, many=True)
        for row in serializer_employee.data:
            get_employees_skills = EmployeeSkill.objects.filter(employee_id=row['id'])
            serializer_employees_skills = EmployeeSkillSerializer(get_employees_skills, many=True)
            emp_dict = {
                'employee_id': row['id'],
                'firstname': row['firstname'],
                'lastname': row['lastname'],
            }
            if get_employees_skills:
                emp_dict['skills'] = serializer_employees_skills.data
            employees_list.append(emp_dict)
        return Response(employees_list, status=HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = Employee.objects.all()
        get_employee = get_object_or_404(queryset, pk=pk)
        serializer_employee = EmployeeSerializer(get_employee)
        get_employee_skills = EmployeeSkill.objects.filter(employee_id=pk)
        serializer_employee_skills = EmployeeSkillSerializer(get_employee_skills, many=True)
        emp_dict = {
            'employee_id': serializer_employee.data['id'],
            'firstname': serializer_employee.data['firstname'],
            'lastname': serializer_employee.data['lastname'],
            'skills': serializer_employee_skills.data,
        }
        return Response(emp_dict, status=HTTP_200_OK)


class GetSkillWeightViewSet(viewsets.ViewSet):
    def update(self, request):
        weight = exponential_weight_algorithm(request)
        return Response([i for i in weight])
