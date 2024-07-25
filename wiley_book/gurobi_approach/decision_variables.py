from gurobipy import GRB
class variables:
    def __init__(self, data):
        self.active = [0 for _ in range(len(data))]
        self.started = [0 for _ in range(len(data))]
        self.output = [0 for _ in range(len(data))]

    def create_variables(self, model, data):
        for t in data['types']:
            self.active[t] = [model.addVar(0, data[f'availability[{t}]'], vtype=GRB.CONTINUOUS, name=f'active_{t}_{time}') for time in data['time_slots']] # var[f'active_{t}']
            self.started[t] = [model.addVar(0, data[f'availability[{t}]'], vtype=GRB.CONTINUOUS, name=f'started_{t}_{time}') for time in data['time_slots']] # var[f'started_{t}'] 
            self. output[t] = [model.addVar(0, GRB.INFINITY, vtype=GRB.CONTINUOUS, name=f'output_{t}_{time}') for time in data['time_slots']] # var[f'output_{t}'] 

        model.update()  # Integrate new variables into the model