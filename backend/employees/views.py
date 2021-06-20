from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated

from employees.models import Employee, EmployeeSkill
from employees.serializer import EmployeeSerializer, EmployeeSkillSerializer, AddEditEmployeeSkillSerializer
from algorithms.algorithms import exponential_weight_algorithm, normalized_weight_algorithm
from .responses import employee_response_list
from skills.models import Skill


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
        get_employees = Employee.objects.all().values('id', 'firstname', 'lastname')
        for row in get_employees:
            get_employees_skills = EmployeeSkill.objects\
                .filter(employee_id=row['id'])\
                .values('seniority_level',
                        'skill_id'
                        )
            emp_dict = row
            if get_employees_skills:
                emp_dict['skills'] = get_employees_skills
            else:
                emp_dict['skills'] = []
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
        queryset = Employee.objects.all().values('id', 'firstname', 'lastname')
        get_employee = get_object_or_404(queryset, pk=pk)
        get_employee_skills = EmployeeSkill.objects.filter(employee_id=pk).values('seniority_level',
                                                                                  'skill_id')
        emp_dict = {
            'employee_id': get_employee['id'],
            'firstname': get_employee['firstname'],
            'lastname': get_employee['lastname'],
            'skills': get_employee_skills,
        }
        return Response(emp_dict, status=HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Method to add skills to employee",
        operation_summary="Add skills to employee",
        tags=['Employees Skills'],
        manual_parameters=[openapi.Parameter('emp_id',
                                             openapi.IN_PATH,
                                             description="id of Employee",
                                             type=openapi.TYPE_INTEGER)],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'data': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'skill_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='0'),
                            'seniority_level': openapi.Schema(type=openapi.TYPE_INTEGER, description='0'),
                        }
                    )
                )
            }
        ),
        responses=employee_response_list['add_employee_skills'])
    def update(self, request, emp_id=None):
        created_ids = []
        query_emp = Employee.objects.filter(pk=emp_id).first()
        if not query_emp:
            return Response('Employee not found', status=HTTP_404_NOT_FOUND)
        for i in request.data['data']:
            query_skill = Skill.objects.filter(pk=i['skill_id']).first()
            if not query_skill:
                return Response('Skill not found', status=HTTP_404_NOT_FOUND)

            emp_skill_model = EmployeeSkill.objects\
                .filter(employee_id=emp_id)\
                .filter(skill_id=i['skill_id'])\
                .first()
            if emp_skill_model:
                return Response('Skill already exists', status=HTTP_400_BAD_REQUEST)

            new_model = AddEditEmployeeSkillSerializer(data=i)
            if new_model.is_valid():
                new_model.save(employee_id=query_emp, skill_id=query_skill)
                created_ids.append(new_model.data['id'])
            else:
                return Response('Incorrect data', status=HTTP_400_BAD_REQUEST)
        return Response({'Created ids': created_ids}, status=HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Method to edit employee skill",
        operation_summary="Edit employee skill",
        tags=['Employees Skills'],
        manual_parameters=[openapi.Parameter('emp_id',
                                             openapi.IN_PATH,
                                             description="id of Employee",
                                             type=openapi.TYPE_INTEGER),
                           openapi.Parameter('skill_id',
                                             openapi.IN_PATH,
                                             description="id of Skill",
                                             type=openapi.TYPE_INTEGER)
                           ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'seniority_level': openapi.Schema(type=openapi.TYPE_INTEGER, description='0'),
            }
        ),
        responses=employee_response_list['add_employee_skills'])
    def partial_update(self, request, emp_id, skill_id):
        query_emp = Employee.objects.filter(pk=emp_id).first()
        if not query_emp:
            return Response('Employee not found', status=HTTP_404_NOT_FOUND)
        query_skill = Skill.objects.filter(pk=skill_id).first()
        if not query_skill:
            return Response('Skill not found', status=HTTP_404_NOT_FOUND)

        model = EmployeeSkill.objects.filter(employee_id=emp_id).filter(skill_id=skill_id).first()
        if not model:
            return Response('Employee with current skill_id not found', status=HTTP_404_NOT_FOUND)

        serializer = AddEditEmployeeSkillSerializer(model, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'Edited id': model.id}, status=HTTP_200_OK)
        else:
            return Response('Incorrect data', status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Method to delete employee skill",
        operation_summary="Delete employee skill",
        tags=['Employees Skills'],
        manual_parameters=[openapi.Parameter('emp_id',
                                             openapi.IN_PATH,
                                             description="id of Employee",
                                             type=openapi.TYPE_INTEGER),
                           openapi.Parameter('skill_id',
                                             openapi.IN_PATH,
                                             description="id of Skill",
                                             type=openapi.TYPE_INTEGER)
                           ],
        responses=employee_response_list['delete_employee_skills'])
    def destroy(self, request, emp_id, skill_id):
        query_emp = Employee.objects.filter(pk=emp_id).first()
        if not query_emp:
            return Response('Employee not found', status=HTTP_404_NOT_FOUND)
        query_skill = Skill.objects.filter(pk=skill_id).first()
        if not query_skill:
            return Response('Skill not found', status=HTTP_404_NOT_FOUND)

        model = EmployeeSkill.objects.filter(employee_id=emp_id).filter(skill_id=skill_id).first()
        id = model.id
        if not model:
            return Response('Employee with current skill_id not found', status=HTTP_404_NOT_FOUND)
        else:
            model.delete()
        return Response({'Deleted id': id}, status=HTTP_200_OK)


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
