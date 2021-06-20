from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated

from employees.models import Employee, EmployeeSkill
from employees.serializer import EmployeeSerializer, EmployeeSkillSerializer
from algorithms.algorithms import exponential_weight_algorithm, normalized_weight_algorithm
from .responses import employee_response_list


class EmployeesViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,]

    @swagger_auto_schema(
        operation_description="Method GET to get all employees",
        operation_summary="Get all employees",
        tags=['Employees'],
        responses=employee_response_list['employees'])
    def list(self, request):
        queryset = Employee.objects.all()
        serializer = EmployeeSerializer(queryset, many=True)
        return Response({'data': serializer.data})

    @swagger_auto_schema(
        operation_description="Method GET to get one employee",
        operation_summary="Get one employee",
        tags=['Employees'],
        manual_parameters=[openapi.Parameter('id',
                                             openapi.IN_PATH,
                                             description="id of Employee",
                                             type=openapi.TYPE_INTEGER)],
        responses={'200': EmployeeSerializer},)
    def retrieve(self, request, pk=None):
        queryset = Employee.objects.all()
        employee = get_object_or_404(queryset, pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)


class EmployeeSkillViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        operation_description="Method GET to get all employees skills",
        operation_summary="Get all employees skills",
        tags=['Employees Skills'],
        responses=employee_response_list['employees_skills'])
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
        return Response({'data': employees_list}, status=HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Method GET to get employee skills",
        operation_summary="Get employee skills",
        tags=['Employees Skills'],
        manual_parameters=[openapi.Parameter('id',
                                             openapi.IN_PATH,
                                             description="id of Employee",
                                             type=openapi.TYPE_INTEGER)],
        responses=employee_response_list['employee_skills'])
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
    @swagger_auto_schema(
        operation_description="Calculate correspondence of employee skills to requested vacation",
        operation_summary="Calculate correspondence of employee skills to requested vacation",
        tags=['Employees Skills'],
        manual_parameters=[openapi.Parameter(name='algorithm_name',
                                             in_=openapi.IN_QUERY,
                                             description="Choose an algorithm for calculation",
                                             required=False,
                                             type=openapi.TYPE_STRING,
                                             enum=['exponential', 'normalized'],
                                             default='exponential',
                                             )
                           ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'data': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='0'),
                            'seniority': openapi.Schema(type=openapi.TYPE_INTEGER, description='0'),
                            'is_main': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='true'),
                        }
                    )
                )
            }
        )
    )
    def create(self, request):
        algorithm_name = request.query_params['algorithm_name']
        warning = None
        weight_result = []

        if not algorithm_name or algorithm_name not in ['exponential', 'normalized']:
            warning = 'Algorithm name not provided or incorrect. Exponential algorithm is used'
        if algorithm_name == 'normalized':
            weight = normalized_weight_algorithm(request)
        else:
            weight = exponential_weight_algorithm(request)

        if not weight:
            return Response('Skills not found', status=HTTP_404_NOT_FOUND)

        for result in weight:
            emp = Employee.objects.get(pk=result['id'])
            query_dict = {
                'id': result['id'],
                'name': f'{emp.firstname} {emp.lastname}',
                'skills': [],
                'weight': result['weight'],
            }
            list_of_skills = [skill_in_request['id'] for skill_in_request in request.data['data']]
            query_skill = EmployeeSkill.objects.\
                filter(employee_id_id=result['id']).\
                filter(skill_id__in=list_of_skills).select_related('skill').values('skill_id',
                                                                                   'seniority_level')

            if query_skill:
                query_dict['skills'] = [row for row in query_skill]
            weight_result.append(query_dict)
        return Response({'data': weight_result, 'warning': warning})
