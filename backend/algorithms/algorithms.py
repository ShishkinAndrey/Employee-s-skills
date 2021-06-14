from employees.models import EmployeeSkill, Employee

import math



# class RequestSkillData:
#     def __init__(self, s_id, seniority, is_main=None):
#         self.id = s_id
#         self.seniority = seniority
#         self.is_main = is_main
#
#
# class EmployeeSkillData:
#     def __init__(self, e_id):
#         self.id = e_id
#         self.skills = {}
#
#     def add_skill(self, s_id, seniority):
#         self.skills[s_id] = RequestSkillData(s_id, seniority)
#
#     def get_skill(self, s_id):
#         return self.skills.get(s_id, None)
#
# request_skill_main_coef = 1.0
# request_skill_optional_coef = 0.2


def exponential_weight_algorithm(request):
    skills_list = [i['id'] for i in request.data]
    emp_skills = EmployeeSkill.objects.filter(skill_id__id__in=skills_list)

    # if not emp_skills:
    #     return not_found('Skills not found')
    query_dict: dict = {}
    k_optional = 1.2
    request_data = request.data

    for row in emp_skills:
        if row.employee_id.id in query_dict.keys():
            query_dict[row.employee_id.id][row.skill_id.id] = row.seniority_level
        else:
            query_dict[row.employee_id.id] = {row.skill_id.id: row.seniority_level, 'weight': 1}

    for skill_request in request_data:
        skill = skill_request['id']
        seniority = skill_request['seniority']
        is_main = skill_request['is_main']
        for emp_id in query_dict:
            if skill in query_dict[emp_id].keys():
                if is_main:
                    if seniority-query_dict[emp_id][skill] > 0:
                        query_dict[emp_id]['weight'] *= math.exp((query_dict[emp_id][skill] - seniority)
                                                                 / seniority)
                    else:
                        query_dict[emp_id]['weight'] *= 1 + (query_dict[emp_id][skill] - seniority) / 10

                if not is_main:
                    if seniority - query_dict[emp_id][skill] > 0:
                        query_dict[emp_id]['weight'] *= math.exp((query_dict[emp_id][skill] - seniority)
                                                                 / seniority) * k_optional
                    else:
                        query_dict[emp_id]['weight'] *= k_optional
            else:
                if type(is_main) == bool:
                    query_dict[emp_id]['weight'] *= math.exp(-1)
    # normalization

    min_res = min(query_dict.items(), key=lambda x: x[1]['weight'])[1]['weight']
    max_res = max(query_dict.items(), key=lambda x: x[1]['weight'])[1]['weight']
    delta = max_res - min_res

    for i in query_dict:
        if delta != 0:
            query_dict[i]['weight'] = (query_dict[i]['weight'] - min_res) / delta
        else:
            query_dict[i]['weight'] = 1.0

    result = [{'id': i, 'weight': query_dict[i]['weight']} for i in query_dict if query_dict[i]['weight'] != 0]
    return result


# def normalized_weight_algorithm(session: Session, request: Request) -> list:
#     s_requests = request.json['data']
#     request_list = [RequestSkillData(s['id'], s['seniority'], s['is_main']) for s in s_requests]
#     # gather employee data into single instance for more convenient usage in cycle
#     e_skills: dict = {}
#     all_employee_skills = session.query(EmployeeSkill).all()
#     if not all_employee_skills:
#         return not_found('Skills not found')
#
#     for e_skill in all_employee_skills:
#         e_id = e_skill.employee_id
#
#         if e_id not in e_skills.keys():
#             e_skills[e_id] = EmployeeSkillData(e_id)
#         e_skills[e_id].add_skill(e_skill.flat_skill_id, e_skill.seniority_level)
#
#     results = []
#     for e_key in e_skills.keys():
#         employee = e_skills[e_key]
#         temp_main: list = []
#         temp_opt: list = []
#         for s_request in request_list:
#             if s_request.is_main:
#                 cur_temp_ref = temp_main
#                 cur_coef = request_skill_main_coef
#             else:
#                 cur_temp_ref = temp_opt
#                 cur_coef = request_skill_optional_coef
#
#             e_skill = employee.get_skill(s_request.id)
#             if e_skill is None:
#                 cur_temp_ref.append(0)
#             else:
#                 cur_temp_ref.append((e_skill.seniority - s_request.seniority) * cur_coef + 3)
#
#         weight_sums = [
#             sum((temp_data * temp_data) / (len(temp_list) * 5) for temp_data in temp_list)
#             for temp_list in (temp_main, temp_opt)
#         ]
#         results.append({'id': employee.id,
#                         'weight': sum(weight_sums)})
#
#     # normalization
#     min_r = min(results, key=lambda x: x['weight'])['weight']
#     max_r = max(results, key=lambda x: x['weight'])['weight']
#     delta = max_r - min_r
#     for r in results:
#         if delta != 0:
#             r['weight'] = (r['weight'] - min_r) / delta
#         else:
#             r['weight'] = 1.0
#     final_result = [r for r in results if r['weight'] != 0]
#     return final_result
