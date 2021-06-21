from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated

from algorithms.models import Preset, RequestSkill
from algorithms.serializer import PresetSerializer, RequestSkillSerializer, AddEditRequestSkillSerializer
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

    @swagger_auto_schema(
        operation_description="Method to add new preset",
        operation_summary="Add new preset",
        tags=['Presets'],
        request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                'skills': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'skill_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='0'),
                            'seniority_level': openapi.Schema(type=openapi.TYPE_INTEGER, description='0'),
                            'is_main': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='0'),
                        }
                    )
                )
            }
        ),
        responses=preset_response_list['add_preset'])
    def create(self, request):
        new_preset = PresetSerializer(data=request.data)
        if new_preset.is_valid():
            for i in request.data['skills']:
                new_request_skill = AddEditRequestSkillSerializer(data=i)
                if new_request_skill.is_valid():
                    query_skill = Skill.objects.filter(pk=i['skill_id']).first()
                    if not query_skill:
                        return Response('Skill not found', status=HTTP_404_NOT_FOUND)
                    new_preset.save()
                    added_preset = Preset.objects.last()
                    new_request_skill.save(preset_id=added_preset, skill_id=query_skill)
                else:
                    return Response('Incorrect request skill data', status=HTTP_400_BAD_REQUEST)
            return Response({'Created preset id': {added_preset.id}}, status=HTTP_201_CREATED)
        return Response('Incorrect preset data', status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Method to add skills to preset",
        operation_summary="Add skills to preset",
        tags=['Presets'],
        manual_parameters=[openapi.Parameter('preset_id',
                                             openapi.IN_PATH,
                                             description="id of Preset",
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
                            'is_main': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='0'),
                        }
                    )
                )
            }
        ),
        responses=preset_response_list['add_skill_preset'])
    def update(self, request, preset_id=None):
        created_ids = []
        query_preset = Preset.objects.filter(pk=preset_id).first()
        if not query_preset:
            return Response('Preset not found', status=HTTP_404_NOT_FOUND)
        for i in request.data['data']:
            query_skill = Skill.objects.filter(pk=i['skill_id']).first()
            if not query_skill:
                return Response('Skill not found', status=HTTP_404_NOT_FOUND)

            emp_skill_model = RequestSkill.objects\
                .filter(preset_id=preset_id)\
                .filter(skill_id=i['skill_id'])\
                .first()
            if emp_skill_model:
                return Response('Skill in preset already exists', status=HTTP_400_BAD_REQUEST)

            new_model = AddEditRequestSkillSerializer(data=i)
            if new_model.is_valid():
                new_model.save(preset_id=query_preset, skill_id=query_skill)
                created_ids.append(new_model.data['id'])
            else:
                return Response('Incorrect data', status=HTTP_400_BAD_REQUEST)
        return Response({'Created ids': created_ids}, status=HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Method to edit preset skill",
        operation_summary="Edit preset skill",
        tags=['Presets'],
        manual_parameters=[openapi.Parameter('preset_id',
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
                'is_main': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='0'),
            }
        ),
        responses=preset_response_list['edit_preset_skills']
        )
    def partial_update(self, request, preset_id, skill_id):
        query_preset = Preset.objects.filter(pk=preset_id).first()
        if not query_preset:
            return Response('Preset not found', status=HTTP_404_NOT_FOUND)
        query_skill = Skill.objects.filter(pk=skill_id).first()
        if not query_skill:
            return Response('Skill not found', status=HTTP_404_NOT_FOUND)

        model = RequestSkill.objects.filter(preset_id=preset_id).filter(skill_id=skill_id).first()
        if not model:
            return Response('Preset with current skill_id not found', status=HTTP_404_NOT_FOUND)

        serializer = AddEditRequestSkillSerializer(model, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'Edited id': model.id}, status=HTTP_200_OK)
        else:
            return Response('Incorrect data', status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Method to delete preset",
        operation_summary="Delete preset",
        tags=['Presets'],
        manual_parameters=[openapi.Parameter('preset_id',
                                             openapi.IN_PATH,
                                             description="id of Employee",
                                             type=openapi.TYPE_INTEGER),
                           ],
        responses=preset_response_list['delete_preset'])
    def destroy(self, request, preset_id):
        query_preset = Preset.objects.filter(pk=preset_id).first()
        if not query_preset:
            return Response('Preset not found', status=HTTP_404_NOT_FOUND)
        id = query_preset.id
        query_preset.delete()
        return Response({'Deleted id': id}, status=HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Method to delete skill in preset",
        operation_summary="Delete skill in preset",
        tags=['Presets'],
        manual_parameters=[openapi.Parameter('preset_id',
                                             openapi.IN_PATH,
                                             description="id of Employee",
                                             type=openapi.TYPE_INTEGER),
                           openapi.Parameter('skill_id',
                                             openapi.IN_PATH,
                                             description="id of Skill",
                                             type=openapi.TYPE_INTEGER)
                           ],
        responses=preset_response_list['delete_skill_preset'])
    def destroy_skill(self, request, preset_id, skill_id):
        query_preset = Preset.objects.filter(pk=preset_id).first()
        if not query_preset:
            return Response('Preset not found', status=HTTP_404_NOT_FOUND)
        query_skill = Skill.objects.filter(pk=skill_id).first()
        if not query_skill:
            return Response('Skill not found', status=HTTP_404_NOT_FOUND)

        model = RequestSkill.objects.filter(preset_id=preset_id).filter(skill_id=skill_id).first()
        id = model.id
        if not model:
            return Response('Preset with current skill_id not found', status=HTTP_404_NOT_FOUND)
        else:
            model.delete()
        return Response({'Deleted id': id}, status=HTTP_200_OK)
