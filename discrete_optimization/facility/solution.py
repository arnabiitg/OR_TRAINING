import math
from ortools.linear_solver import pywraplp
import random

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def calculate_cost(facilities, customers, dist, assignment):
    used = [0]*len(facilities)
    for facility_index in assignment:
        used[facility_index] = 1

    # calculate the cost of the assignment
    total_cost = sum([f.setup_cost*used[f.index] for f in facilities])
    for customer in customers:
        total_cost += length(customer.location, facilities[assignment[customer.index]].location)
    
    return total_cost

def trivial_solution(facilities, customers):
    facility_index = 0
    solution = [-1]*len(customers)
    capacity_remaining = [f.capacity for f in facilities]
    for customer in customers:
        if capacity_remaining[facility_index] >= customer.demand:
            solution[customer.index] = facility_index
            capacity_remaining[facility_index] -= customer.demand
        else:
            facility_index += 1
            assert capacity_remaining[facility_index] >= customer.demand
            solution[customer.index] = facility_index
            capacity_remaining[facility_index] -= customer.demand

    return trivial_solution

def two_opt_heuristic(facilities, customers, dist, init_solution):
    best_solution = init_solution
    best_cost = calculate_cost(facilities, customers, dist, best_solution)
    
    improved = True
    while improved:
        improved = False
        for i in range(len(customers)):
            for j in range(i + 1, len(customers)):
                new_solution = best_solution[:]
                cap_1 = facilities[new_solution[i]].capacity - customers[i].demand + customers[j].demand
                cap_2 = facilities[new_solution[j]].capacity - customers[j].demand + customers[i].demand
                if cap_1 >= 0 and cap_2 >= 0:
                    new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
                    
                    new_cost = calculate_cost(facilities, customers, dist, new_solution)
                    if new_cost < best_cost:
                        best_solution = new_solution
                        best_cost = new_cost
                        improved = True
    
    return best_cost, best_solution

def main(facilities, customers):

    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return
    
    # Calculate the distance matrix
    dist = [[length(customers[i].location,facilities[j].location) for j in range(len(facilities))] for i in range(len(customers))]
    
    # Call the heuristic function
    # init_solution = trivial_solution(facilities, customers)
    # return calculate_cost(facilities, customers, dist, init_solution), init_solution
    # return two_opt_heuristic(facilities, customers, dist, init_solution)
    # Define the decison variables
    c = []
    for i in range(len(customers)):
        row = []
        for j in range(len(facilities)):
            row.append(solver.BoolVar(f'c[{i}][{j}]'))
        c.append(row)
    v = [solver.BoolVar(f'v[{j}]') for j in range(len(facilities))]
    
    # Add constraints
    for i in range(len(customers)):
        solver.Add(sum([c[i][j] for j in range(len(facilities))]) == 1)

    for j in range(len(facilities)):
        solver.Add(sum([c[i][j]*customers[i].demand for i in range(len(customers))]) <= facilities[j].capacity)

    for j in range(len(facilities)):
        for i in range(len(customers)):
            # solver.Add(sum([c[i][j] for i in range(len(customers))]) <= v[j]*len(customers))
            solver.Add(c[i][j] <= v[j])
        
    # Define the objective function
    objective = solver.Objective()
    for i in range(len(customers)):
        for j in range(len(facilities)):
            objective.SetCoefficient(c[i][j], dist[i][j])

    for j in range(len(facilities)):
        objective.SetCoefficient(v[j],facilities[j].setup_cost)
    
    # for j in range(len(facilities)):
    #     objective.SetCoefficient(sum([c[i][j] for i in range(len(customers))]), facilities[j].setup_cost)
    objective.SetMinimization()
    solver.set_time_limit(900*1000)
    status = solver.Solve()
    solution = [0 for _ in range(len(customers))]
    # if status == pywraplp.Solver.OPTIMAL:
        
    # else:
    #     print('The problem does not have an optimal solution.')
    for i in range(len(customers)):
            for j in range(len(facilities)):
                if c[i][j].solution_value() == True:
                    solution[i] = j
                    break
    return solver.Objective().Value(), solution
