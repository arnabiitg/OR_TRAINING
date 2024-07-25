from gurobipy import GRB, quicksum
class Objective:
    def obj_fun(self, model, variables, data):
        # Define the objective function
        objective = model.setObjective(
            quicksum(
                variables.active[t][time] * (
                    data[f'power_plant_data[{t}]']['Cost_per_hour_at_minimum'] 
                    - data[f'power_plant_data[{t}]']['Minimum_level_(MW)'] * data[f'power_plant_data[{t}]']['Cost_per_hour_per_megawatt_above_minimum']
                ) + variables.output[t][time] * data[f'power_plant_data[{t}]']['Cost_per_hour_per_megawatt_above_minimum'] 
                + variables.started[t][time] * data[f'power_plant_data[{t}]']['Fixed_cost']
                for t in data['types'] for time in data['time_slots']
            ), GRB.MINIMIZE
        )

        # Optimize the model
        model.optimize()

        # Print the results
        if model.status == GRB.OPTIMAL:
            print('The Optimal Cost is:', model.ObjVal)
            for time in data['time_slots']:
                print(f"Time slot {time}:")
                for t in data['types']:
                    print(f"  Type {t} - Active: {variables.active[t][time].X}, Output: {variables.output[t][time].X}")
        else:
            print('No Optimal Solution found.')