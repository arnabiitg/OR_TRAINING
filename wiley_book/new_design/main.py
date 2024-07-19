from ortools.linear_solver import pywraplp
from decision_variables import input
from constraints import Constraints
from objective import Objective
from input_data import Read
solver = pywraplp.Solver.CreateSolver('SCIP')

def solution(id):
# read data
    read = Read(id)
    data = read.read_data() 
# Create decision Varibles
    variables = input(id)
    var = variables.create_variables(solver, data)

# Create the constraints
    constraint = Constraints(id)
    constraint.add_const(solver, var, data)

# Create Objective and solve
    obj = Objective(id)
    obj.obj_fun(solver,var, data)

def main():
    id = 13.1
    solution(id)

if __name__ == '__main__':
    main()