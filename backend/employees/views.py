from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from employees.models import Employee
from employees.serializer import EmployeeSerializer


class EmployeesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, ]
