class Constraints:
    def add_const(self, model, variables, data):
        # Starting Constraints
        for time in data['time_slots']:
            if time == 0:
                for t in data['types']:
                    model.addConstr(variables.started[t][time] >= variables.active[t][time], name=f'started_{t}_time{time}_constraint')
            else:
                for t in data['types']:
                    model.addConstr(variables.started[t][time] >= variables.active[t][time] - variables.active[t][time-1], name=f'started_{t}_time{time}_constraint')

        # Output Constraints
        for time in data['time_slots']:
            for t in data['types']:
                model.addConstr(variables.output[t][time] >= variables.active[t][time] * data[f'power_plant_data[{t}]']["Minimum_level_(MW)"], name=f'output_min_{t}_time{time}_constraint')
                model.addConstr(variables.output[t][time] <= variables.active[t][time] * data[f'power_plant_data[{t}]']["Maximum_level_(MW)"], name=f'output_max_{t}_time{time}_constraint')

        # Demand Constraints with 15% reserve
        for time in data['time_slots']:
            model.addConstr(sum(variables.output[t][time] for t in data['types']) == data[f'demands[{time}]'], name=f'demand_{time}_constraint')
            model.addConstr(sum(variables.active[t][time] * data[f'power_plant_data[{t}]']['Maximum_level_(MW)'] for t in data['types']) >= 1.15 * data[f'demands[{time}]'], name=f'reserve_{time}_constraint')