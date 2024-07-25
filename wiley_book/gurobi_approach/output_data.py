from gurobipy import GRB
import pandas as pd
class Output:
    def write_output(self, model, vars, data):
        # Extracting the results and saving them into an Excel sheet
        if model.status == GRB.OPTIMAL:
            print('The Optimal Cost is:', model.ObjVal)

            results = {
                'Time Slot': [],
                'Type': [],
                'Active': [],
                'Output': []
            }

            for time in data['time_slots']:
                for t in data['types']:
                    results['Time Slot'].append(time)
                    results['Type'].append(t)
                    results['Active'].append(vars.active[t][time].X)
                    results['Output'].append(vars.output[t][time].X)

            df = pd.DataFrame(results)
            df.to_excel('./data/optimization_results.xlsx', index=False)
            print('Results have been written to optimization_results.xlsx')
        else:
            print('No Optimal Solution found.')