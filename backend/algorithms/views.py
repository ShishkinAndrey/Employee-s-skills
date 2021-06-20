from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated

from algorithms.models import Preset, RequestSkill
from algorithms.serializer import PresetSerializer, RequestSkillSerializer
from .responses import preset_response_list
from skills.models import Skill


class PresetViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        operation_description="Method GET to get all presets",
        operation_summary="Get all presets",
        tags=['Presets'],
        responses=preset_response_list['get_presets'])
    def list(self, request):
        presets_list = []
        get_presets = Preset.objects.all().values('id', 'name', 'description')
        for row in get_presets:
            get_request_skills = RequestSkill.objects\
                .filter(preset_id=row['id'])\
                .values('skill_id',
                        'seniority_level',
                        'is_main'
                        )

            if get_request_skills:
                row['skills'] = get_request_skills
                for skill in row['skills']:
                    get_skills = Skill.objects.filter(pk=skill['skill_id']).first()
                    skill['skill'] = get_skills.skill
                    skill['competency'] = get_skills.competency
            else:
                row['skills'] = []

            presets_list.append(row)
        return Response({'data': presets_list}, status=HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Method GET to get one preset",
        operation_summary="Get one preset",
        tags=['Presets'],
        manual_parameters=[openapi.Parameter('id',
                                             openapi.IN_PATH,
                                             description="id of Preset",
                                             type=openapi.TYPE_INTEGER)],
        responses=preset_response_list['get_one_preset'])
    def retrieve(self, request, pk=None):
        queryset = Preset.objects.all().values('id', 'name', 'description')
        get_preset = get_object_or_404(queryset, pk=pk)

        get_request_skills = RequestSkill.objects \
            .filter(preset_id=get_preset['id']) \
            .values('skill_id',
                    'seniority_level',
                    'is_main'
                    )

        if get_request_skills:
            get_preset['skills'] = get_request_skills
            for skill in get_preset['skills']:
                get_skills = Skill.objects.filter(pk=skill['skill_id']).first()
                skill['skill'] = get_skills.skill
                skill['competency'] = get_skills.competency
        else:
            get_preset['skills'] = []

        return Response(get_preset, status=HTTP_200_OK)

    # @swagger_auto_schema(
    #     operation_description="Method to add skills to employee",
    #     operation_summary="Add skills to employee",
    #     tags=['Employees Skills'],
    #     manual_parameters=[openapi.Parameter('emp_id',
    #                                          openapi.IN_PATH,
    #                                          description="id of Employee",
    #                                          type=openapi.TYPE_INTEGER)],
    #     request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         properties={
    #             'data': openapi.Schema(
    #                 type=openapi.TYPE_ARRAY,
    #                 items=openapi.Schema(
    #                     type=openapi.TYPE_OBJECT,
    #                     properties={
    #                         'skill_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='0'),
    #                         'seniority_level': openapi.Schema(type=openapi.TYPE_INTEGER, description='0'),
    #                     }
    #                 )
    #             )
    #         }
    #     ),
    #     responses=employee_response_list['add_employee_skills'])
    # def update(self, request, emp_id=None):
    #     created_ids = []
    #     query_emp = Employee.objects.filter(pk=emp_id).first()
    #     if not query_emp:
    #         return Response('Employee not found', status=HTTP_404_NOT_FOUND)
    #     for i in request.data['data']:
    #         query_skill = Skill.objects.filter(pk=i['skill_id']).first()
    #         if not query_skill:
    #             return Response('Skill not found', status=HTTP_404_NOT_FOUND)
    #
    #         emp_skill_model = EmployeeSkill.objects\
    #             .filter(employee_id=emp_id)\
    #             .filter(skill_id=i['skill_id'])\
    #             .first()
    #         if emp_skill_model:
    #             return Response('Skill already exists', status=HTTP_400_BAD_REQUEST)
    #
    #         new_model = AddEditEmployeeSkillSerializer(data=i)
    #         if new_model.is_valid():
    #             new_model.save(employee_id=query_emp, skill_id=query_skill)
    #             created_ids.append(new_model.data['id'])
    #         else:
    #             return Response('Incorrect data', status=HTTP_400_BAD_REQUEST)
    #     return Response({'Created ids': created_ids}, status=HTTP_200_OK)
    #
    # @swagger_auto_schema(
    #     operation_description="Method to edit employee skill",
    #     operation_summary="Edit employee skill",
    #     tags=['Employees Skills'],
    #     manual_parameters=[openapi.Parameter('emp_id',
    #                                          openapi.IN_PATH,
    #                                          description="id of Employee",
    #                                          type=openapi.TYPE_INTEGER),
    #                        openapi.Parameter('skill_id',
    #                                          openapi.IN_PATH,
    #                                          description="id of Skill",
    #                                          type=openapi.TYPE_INTEGER)
    #                        ],
    #     request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         properties={
    #             'seniority_level': openapi.Schema(type=openapi.TYPE_INTEGER, description='0'),
    #         }
    #     ),
    #     responses=employee_response_list['add_employee_skills'])
    # def partial_update(self, request, emp_id, skill_id):
    #     query_emp = Employee.objects.filter(pk=emp_id).first()
    #     if not query_emp:
    #         return Response('Employee not found', status=HTTP_404_NOT_FOUND)
    #     query_skill = Skill.objects.filter(pk=skill_id).first()
    #     if not query_skill:
    #         return Response('Skill not found', status=HTTP_404_NOT_FOUND)
    #
    #     model = EmployeeSkill.objects.filter(employee_id=emp_id).filter(skill_id=skill_id).first()
    #     if not model:
    #         return Response('Employee with current skill_id not found', status=HTTP_404_NOT_FOUND)
    #
    #     serializer = AddEditEmployeeSkillSerializer(model, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'Edited id': model.id}, status=HTTP_200_OK)
    #     else:
    #         return Response('Incorrect data', status=HTTP_400_BAD_REQUEST)
    #
    # @swagger_auto_schema(
    #     operation_description="Method to delete employee skill",
    #     operation_summary="Delete employee skill",
    #     tags=['Employees Skills'],
    #     manual_parameters=[openapi.Parameter('emp_id',
    #                                          openapi.IN_PATH,
    #                                          description="id of Employee",
    #                                          type=openapi.TYPE_INTEGER),
    #                        openapi.Parameter('skill_id',
    #                                          openapi.IN_PATH,
    #                                          description="id of Skill",
    #                                          type=openapi.TYPE_INTEGER)
    #                        ],
    #     responses=employee_response_list['delete_employee_skills'])
    # def destroy(self, request, emp_id, skill_id):
    #     query_emp = Employee.objects.filter(pk=emp_id).first()
    #     if not query_emp:
    #         return Response('Employee not found', status=HTTP_404_NOT_FOUND)
    #     query_skill = Skill.objects.filter(pk=skill_id).first()
    #     if not query_skill:
    #         return Response('Skill not found', status=HTTP_404_NOT_FOUND)
    #
    #     model = EmployeeSkill.objects.filter(employee_id=emp_id).filter(skill_id=skill_id).first()
    #     id = model.id
    #     if not model:
    #         return Response('Employee with current skill_id not found', status=HTTP_404_NOT_FOUND)
    #     else:
    #         model.delete()
    #     return Response({'Deleted id': id}, status=HTTP_200_OK)
