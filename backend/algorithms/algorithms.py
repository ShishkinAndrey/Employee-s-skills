from employees.models import EmployeeSkill, Employee

import math


def exponential_weight_algorithm(query_request_skill):

    skills_list = [i.skill_id.id for i in query_request_skill]
    emp_skills = EmployeeSkill.objects.filter(skill_id__id__in=skills_list)

    if not emp_skills:
        return []

    query_dict: dict = {}
    k_optional = 1.2

    for row in emp_skills:
        if row.employee_id.id in query_dict.keys():
            query_dict[row.employee_id.id][row.skill_id.id] = row.seniority_level
        else:
            query_dict[row.employee_id.id] = {row.skill_id.id: row.seniority_level, 'weight': 1}

    for skill_request in query_request_skill:
        skill = skill_request.skill_id.id
        seniority = skill_request.seniority_level
        is_main = skill_request.is_main
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
    max_res = max(query_dict.items(), key=lambda x: x[1]['weight'])[1]['weight']

    for i in query_dict:
        query_dict[i]['weight'] = query_dict[i]['weight'] / max_res

    result = [{'id': i, 'weight': query_dict[i]['weight']} for i in query_dict if query_dict[i]['weight'] != 0]
    return result


class RequestSkillData:
    def __init__(self, s_id, seniority, is_main=None):
        self.id = s_id
        self.seniority = seniority
        self.is_main = is_main


class EmployeeSkillData:
    def __init__(self, e_id):
        self.id = e_id
        self.skills = {}

    def add_skill(self, s_id, seniority):
        self.skills[s_id] = RequestSkillData(s_id, seniority)

    def get_skill(self, s_id):
        return self.skills.get(s_id, None)


request_skill_main_coef = 1.0
request_skill_optional_coef = 0.2


def normalized_weight_algorithm(query_request_skill):
    request_list = [RequestSkillData(s.skill_id.id, s.seniority_level, s.is_main) for s in query_request_skill]
    # gather employee data into single instance for more convenient usage in cycle
    e_skills: dict = {}
    skills_list = [i.skill_id.id for i in query_request_skill]
    emp_skills = EmployeeSkill.objects.filter(skill_id__id__in=skills_list)

    for e_skill in emp_skills:
        e_id = e_skill.employee_id.id

        if e_id not in e_skills.keys():
            e_skills[e_id] = EmployeeSkillData(e_id)
        e_skills[e_id].add_skill(e_skill.skill_id.id, e_skill.seniority_level)

    results = []
    for e_key in e_skills.keys():
        employee = e_skills[e_key]
        temp_main: list = []
        temp_opt: list = []
        for s_request in request_list:
            if s_request.is_main:
                cur_temp_ref = temp_main
                cur_coef = request_skill_main_coef
            else:
                cur_temp_ref = temp_opt
                cur_coef = request_skill_optional_coef

            e_skill = employee.get_skill(s_request.id)
            if e_skill is None:
                cur_temp_ref.append(0)
            else:
                cur_temp_ref.append((e_skill.seniority - s_request.seniority + 3) * cur_coef)

        weight_sums = [
            sum((temp_data * temp_data) / (len(temp_list) * 5) for temp_data in temp_list)
            for temp_list in (temp_main, temp_opt)
        ]
        results.append({'id': employee.id,
                        'weight': sum(weight_sums)})

    # normalization
    max_r = max(results, key=lambda x: x['weight'])['weight']
    for r in results:
        r['weight'] = r['weight'] / max_r

    final_result = [r for r in results if r['weight'] != 0]
    return final_result
