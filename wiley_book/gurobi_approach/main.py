from gurobipy import Model
from input_data import input
from decision_variables import variables
from constraints import Constraints
from objective import Objective
from output_data import Output

def Main():
    # Define the Model
    model = Model()

    # Reading the input data
    reader = input()
    data = reader.read_input()

    # Create decision Varibles
    vars = variables(data)
    vars.create_variables(model, data)

    # Create the constraints
    constraint = Constraints()
    constraint.add_const(model, vars, data)

    # Create Objective and solve
    obj = Objective()
    obj.obj_fun(model,vars, data)

    # Output data
    out_data = Output()
    out_data.write_output(model, vars, data)

if __name__ == '__main__':
    Main()