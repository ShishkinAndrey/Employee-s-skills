from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from skills.models import Skill
from skills.serializer import SkillSerializer


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      operation_description="Method GET to get all skills",
                      operation_summary="Get all skills",
                      tags=['Skills'],
                  )
                  )
@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(
                      operation_description="Method GET to get one skill",
                      operation_summary="Get one skill",
                      tags=['Skills'],
                      manual_parameters=[
                          openapi.Parameter(
                              'id', openapi.IN_PATH,
                              description="id of skill",
                              type=openapi.TYPE_INTEGER)
                      ]
                  )
                  )
class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated, ]
