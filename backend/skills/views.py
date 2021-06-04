from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from skills.models import Skill
from skills.serializer import SkillSerializer


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated, ]
