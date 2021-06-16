from drf_yasg import openapi
from rest_framework import status
from employees.serializer import EmployeeSerializer, EmployeeSkillSerializer

employee_response_list = {
    'employees': {
        status.HTTP_200_OK: openapi.Response(
            description="200: Successfully read list of employees",
            examples={
                "application/json":
                    {'data': [
                        {
                            "id": 0,
                            "firstname": "string",
                            "lastname": "string",
                            "employee_email": "user@example.com"
                        }
                    ]
                    }
            },
            schema=EmployeeSerializer
        )
    },
    'employees_skills': {
        status.HTTP_200_OK: openapi.Response(
            description="200: Successfully read list of employees skills",
            examples={
                "application/json":
                    {'data': [
                        {
                            "employee_id": 0,
                            "firstname": "string",
                            "lastname": "string",
                            "skills": [
                                {
                                    "id": 0,
                                    "seniority_level": 0,
                                    "employee_id": 0,
                                    "skill_id": 0
                                }
                            ]
                        }
                    ]
                    }
            }
        )
    },
    'employee_skills': {
        status.HTTP_200_OK: openapi.Response(
            description="200: Successfully read list of employees skills",
            examples={
                "application/json":
                    {
                        "employee_id": 0,
                        "firstname": "string",
                        "lastname": "string",
                        "skills": [
                            {
                                "id": 0,
                                "seniority_level": 0,
                                "employee_id": 0,
                                "skill_id": 0
                            },
                        ]
                    }
            }
        )
    }
}
