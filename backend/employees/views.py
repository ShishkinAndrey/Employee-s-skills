from rest_framework import viewsets, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from employees.models import Employee, EmployeeSkill
from employees.serializer import EmployeeSerializer, EmployeeSkillSerializer


class EmployeesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, ]
#
#
# class EmployeesSkillsViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = EmployeeSkill.objects.all()
#     serializer_class = EmployeeSkillSerializer
#     permission_classes = [IsAuthenticated, ]


# class EmployeesViewSet(views.APIView):
#     def get(self, request, format=None):
#         snippets = Employee.objects.all()
#         serializer = EmployeeSerializer(snippets, many=True)
#         return Response(serializer.data)


# class DetailedEmployeesViewSet(views.APIView):
#     def get_object(self, pk):
#         try:
#             return Employee.objects.get(pk=pk)
#         except Employee.DoesNotExist:
#             raise NotFound
#
#     def get(self, request, pk):
#         snippet = self.get_object(pk)
#         serializer = EmployeeSerializer(snippet)
#         return Response(serializer.data)
