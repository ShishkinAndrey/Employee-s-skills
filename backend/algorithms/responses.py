from drf_yasg import openapi
from rest_framework import status
from employees.serializer import EmployeeSerializer, EmployeeSkillSerializer

preset_response_list = {
    'get_presets': {
        status.HTTP_200_OK: openapi.Response(
            description="200: Successfully read list of presets",
            examples={
                "application/json":
                    {'data': [
                        {
                            "id": 0,
                            "name": "string",
                            "description": "string",
                            "skills": [
                                {
                                    "seniority_level": 0,
                                    "skill_id": 0,
                                    "is_main": True,
                                    "skill": "string",
                                    "competency": "string"
                                }
                            ]
                        }
                    ]
                    }
            }
        )
    },
    'get_one_preset': {
        status.HTTP_200_OK: openapi.Response(
            description="200: Successfully read one preset",
            examples={
                "application/json":
                    {
                        "id": 0,
                        "name": "string",
                        "description": "string",
                        "skills": [
                            {
                                "seniority_level": 0,
                                "skill_id": 0,
                                "is_main": True,
                                "skill": "string",
                                "competency": "string"
                            }
                        ]
                    }
            }
        )
    },
    'add_preset': {
            status.HTTP_200_OK: openapi.Response(
                description="200: Successfully add new preset",
                examples={
                    "application/json":
                        {'Created preset id': 0}
                }
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                            description="404: Not Found",
                            examples={
                                "application/json":
                                    ['Skill not found',
                                     ]
                            }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                                        description="400: Bad Request",
                                        examples={
                                            "application/json":
                                                ['Incorrect preset data',
                                                 'Incorrect request skill data',
                                                 'Incorrect seniority level value'
                                                 ]
                                        }
                        )
        },
    'add_skill_preset': {
                status.HTTP_200_OK: openapi.Response(
                    description="200: Successfully add new preset",
                    examples={
                        "application/json":
                            {'Created preset id': 0}
                    }
                ),
                status.HTTP_404_NOT_FOUND: openapi.Response(
                                description="404: Not Found",
                                examples={
                                    "application/json":
                                        ['Skill not found',
                                         'Preset not found',
                                         ]
                                }
                ),
                status.HTTP_400_BAD_REQUEST: openapi.Response(
                                            description="400: Bad Request",
                                            examples={
                                                "application/json":
                                                    ['Incorrect data',
                                                     'Skill in preset already exists',
                                                     'Incorrect seniority level value'
                                                     ]
                                            }
                            )
            },
    'edit_preset_skills': {
                status.HTTP_200_OK: openapi.Response(
                    description="200: Successfully edit employees skill",
                    examples={
                        "application/json":
                            {'Edited id': 0}
                    }
                ),
                status.HTTP_404_NOT_FOUND: openapi.Response(
                                description="404: Not Found",
                                examples={
                                    "application/json":
                                        ['Employee not found',
                                         'Skill not found',
                                         'Employee with current skill_id not found',
                                         ]
                                }
                ),
                status.HTTP_400_BAD_REQUEST: openapi.Response(
                                            description="400: Bad Request",
                                            examples={
                                                "application/json":
                                                    ['Incorrect data',
                                                     'Incorrect seniority level value']

                                            }
                            )
            },
    'delete_preset': {
                    status.HTTP_200_OK: openapi.Response(
                        description="200: Successfully deleted preset",
                        examples={
                            "application/json":
                                {'Deleted id': 0}
                        }
                    ),
                    status.HTTP_404_NOT_FOUND: openapi.Response(
                                    description="404: Not Found",
                                    examples={
                                        "application/json":
                                            ['Preset not found',
                                             ]
                                    }
                    ),
    },
    'delete_skill_preset': {
                        status.HTTP_200_OK: openapi.Response(
                            description="200: Successfully deleted skill in preset",
                            examples={
                                "application/json":
                                    {'Deleted id': 0}
                            }
                        ),
                        status.HTTP_404_NOT_FOUND: openapi.Response(
                                        description="404: Not Found",
                                        examples={
                                            "application/json":
                                                ['Preset not found',
                                                 'Skill not found',
                                                 'Preset with current skill_id not found',
                                                 ]
                                        }
                        ),
        },
}
