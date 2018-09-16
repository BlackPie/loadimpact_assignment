import math
import re

from pulp import pulp


def get_maintenance_scheme(de_capacity, dm_capacity, data_centers) -> tuple:
    """
    It uses straightforward approach and returns number of DE needed for given capacities and data centers
    """
    best_iteration = 0
    de_saved_best = 0
    de_count = 0

    for i, data_center in enumerate(data_centers):
        de_needed = math.ceil(data_center['servers'] / de_capacity)
        de_count += de_needed
        de_needed_with_dm = math.ceil((data_center['servers'] - dm_capacity) / de_capacity)
        de_saved = de_needed - de_needed_with_dm

        if de_saved > de_saved_best:
            de_saved_best = de_saved
            best_iteration = i

    de_count -= de_saved_best
    return de_count, data_centers[best_iteration]['name']


def get_maintenance_scheme_system_of_equations(de_capacity, dm_capacity, data_centers) -> tuple:
    """
    Creates all combinations of systems of equations and calculates the best one
    """
    data_center_count = len(data_centers)
    result_list = list()

    for i in range(data_center_count):
        de_total = 0

        for j, data_center in enumerate(data_centers):
            if i == j:
                servers_left = data_center['servers'] - dm_capacity

                if not servers_left:
                    de_count = 0
                else:
                    de_count = math.ceil(servers_left / de_capacity)
            else:
                de_count = math.ceil(data_center['servers'] / de_capacity)

            de_total += de_count

        result_list.append((i, de_total))

    data_center_index, de_final_count = min(result_list, key=lambda x: x[1])
    return de_final_count, data_centers[data_center_index]['name']


def get_maintenance_scheme_pulp_optimization(de_capacity, dm_capacity, data_centers) -> tuple:
    """
    Uses PuLP library to find minimal values of equations
    """
    variables = list()

    for i in range(len(data_centers) * 2):
        variable = pulp.LpVariable('x{}'.format(i), lowBound=0, cat='Integer')
        variables.append(variable)

    managers = variables[::2]
    engineers = variables[1::2]
    problem = pulp.LpProblem("Minimize number of engineers", pulp.LpMinimize)
    problem += sum(engineers), 'Z'
    problem += sum(managers) == 1

    for i, data_center in enumerate(data_centers):
        problem += dm_capacity * managers[i] + de_capacity * engineers[i] >= data_center['servers']

    problem.solve()

    for variable in managers:
        if variable.value():
            data_center_id = int(int(re.search(r'\d+', str(variable)).group()) / 2)

    engineer_list = [x.value() for x in engineers]
    return int(sum(engineer_list)), data_centers[data_center_id]['name']
