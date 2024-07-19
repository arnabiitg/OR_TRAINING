from ortools.linear_solver import pywraplp

class Objective:
    def __init__(self,id):
        self.id = id
    def obj_fun(self, solver, var, data):
        if self.id == 9:
            total_cap = solver.Objective()
            years = range(1,6)
            industries = ['coal','steel','transport']
            for year in years:
                for industry in industries:
                    total_cap.SetCoefficient(var['extra_cap'][industry][year],1)


            total_cap.SetMaximization()
            status = solver.Solve()

            if status == pywraplp.Solver.OPTIMAL:
                print('The Optimal Capacity is: ',total_cap.Value())
            else:
                print('No Optimal Solution found.')
        
        elif self.id == 11:
            points = {
                'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0],
                'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3]
            }

            error = solver.Objective()
            for i in range(len(points['x'])):
                error.SetCoefficient(var['z'][i],1)
            
            error.SetMinimization()
            status = solver.Solve()

            if status == pywraplp.Solver.OPTIMAL:
                print('The Optimal Capacity is: ',error.Value())
                for i in range(len(points['x'])):
                    print(f'a_{i}: ',var['a'][i].solution_value(), f'b_{i}: ', var['b'][i].solution_value())
            else:
                print('No Optimal Solution found.')

        elif self.id == 13.1:
            data = {
                "M1": {"Region": "Region_1", "Oil_market": 9, "Delivery_points": 11, "Spirit_market": 34, "Growth_category": "A"},
                "M2": {"Region": "Region_1", "Oil_market": 13, "Delivery_points": 47, "Spirit_market": 411, "Growth_category": "A"},
                "M3": {"Region": "Region_1", "Oil_market": 14, "Delivery_points": 44, "Spirit_market": 82, "Growth_category": "A"},
                "M4": {"Region": "Region_1", "Oil_market": 17, "Delivery_points": 25, "Spirit_market": 157, "Growth_category": "B"},
                "M5": {"Region": "Region_1", "Oil_market": 18, "Delivery_points": 10, "Spirit_market": 5, "Growth_category": "A"},
                "M6": {"Region": "Region_1", "Oil_market": 19, "Delivery_points": 26, "Spirit_market": 183, "Growth_category": "A"},
                "M7": {"Region": "Region_1", "Oil_market": 23, "Delivery_points": 26, "Spirit_market": 14, "Growth_category": "B"},
                "M8": {"Region": "Region_1", "Oil_market": 21, "Delivery_points": 54, "Spirit_market": 215, "Growth_category": "B"},
                "M9": {"Region": "Region_2", "Oil_market": 9, "Delivery_points": 18, "Spirit_market": 102, "Growth_category": "B"},
                "M10": {"Region": "Region_2", "Oil_market": 11, "Delivery_points": 51, "Spirit_market": 21, "Growth_category": "A"},
                "M11": {"Region": "Region_2", "Oil_market": 17, "Delivery_points": 20, "Spirit_market": 54, "Growth_category": "B"},
                "M12": {"Region": "Region_2", "Oil_market": 18, "Delivery_points": 105, "Spirit_market": 0, "Growth_category": "B"},
                "M13": {"Region": "Region_2", "Oil_market": 18, "Delivery_points": 7, "Spirit_market": 6, "Growth_category": "B"},
                "M14": {"Region": "Region_2", "Oil_market": 17, "Delivery_points": 16, "Spirit_market": 96, "Growth_category": "B"},
                "M15": {"Region": "Region_2", "Oil_market": 22, "Delivery_points": 34, "Spirit_market": 118, "Growth_category": "A"},
                "M16": {"Region": "Region_2", "Oil_market": 24, "Delivery_points": 100, "Spirit_market": 112, "Growth_category": "B"},
                "M17": {"Region": "Region_2", "Oil_market": 36, "Delivery_points": 50, "Spirit_market": 535, "Growth_category": "B"},
                "M18": {"Region": "Region_2", "Oil_market": 43, "Delivery_points": 21, "Spirit_market": 8, "Growth_category": "B"},
                "M19": {"Region": "Region_3", "Oil_market": 6, "Delivery_points": 11, "Spirit_market": 53, "Growth_category": "B"},
                "M20": {"Region": "Region_3", "Oil_market": 15, "Delivery_points": 19, "Spirit_market": 28, "Growth_category": "A"},
                "M21": {"Region": "Region_3", "Oil_market": 15, "Delivery_points": 14, "Spirit_market": 69, "Growth_category": "B"},
                "M22": {"Region": "Region_3", "Oil_market": 25, "Delivery_points": 10, "Spirit_market": 65, "Growth_category": "B"},
                "M23": {"Region": "Region_3", "Oil_market": 39, "Delivery_points": 11, "Spirit_market": 27, "Growth_category": "B"}
            }

            retailers = list(data.keys())
            regions = ['Region_1', 'Region_2', 'Region_3']
            categories = ['A', 'B']
            total_deviation = solver.Objective()
            total_deviation.SetCoefficient(var['delivery_break'], 1)
            total_deviation.SetCoefficient(var['spirit_break'], 1)
            for region in regions:
                total_deviation.SetCoefficient(var[f'oil_{region}_break'], 1)
            for category in categories:
                total_deviation.SetCoefficient(var[f'group_break_{category}'], 1)
            total_deviation.SetMinimization()
            # Solve the problem
            status = solver.Solve()

            # Print the results
            if status == pywraplp.Solver.OPTIMAL:
                print('The Optimal Deviation is:', total_deviation.Value())
                for retailer in retailers:
                    if var[f'c_{retailer}_D1'].solution_value() == 1:
                        print(f'Retailer {retailer} is assigned to Division D1')
                    else:
                        print(f'Retailer {retailer} is assigned to Division D2')
            else:
                print('No Optimal Solution found.')

        elif self.id == 15:
            cost = solver.Objective()
            for time in data['time_slots']:
                for t in data['types']:
                    # Cost per hour at minimum level
                    cost.SetCoefficient(var[f'active_{t}'][time], data[f'power_plant_data[{t}]']['Cost_per_hour_at_minimum']
                                        - data[f'power_plant_data[{t}]']['Minimum_level_(MW)'] * data[f'power_plant_data[{t}]']['Cost_per_hour_per_megawatt_above_minimum'])
                    # Additional cost for output above minimum level
                    cost.SetCoefficient(var[f'output_{t}'][time], data[f'power_plant_data[{t}]']['Cost_per_hour_per_megawatt_above_minimum'])
                    # Fixed startup cost
                    cost.SetCoefficient(var[f'started_{t}'][time], data[f'power_plant_data[{t}]']['Fixed_cost'])
                    

            cost.SetMinimization()

            # Solve the problem
            status = solver.Solve()

            # Print the results
            if status == pywraplp.Solver.OPTIMAL:
                print('The Optimal Cost is:', cost.Value())
                for time in data['time_slots']:
                    print(f"Time slot {time}:")
                    for t in data['types']:
                        print(f"  Type {t} - Active: {var[f'active_{t}'][time].solution_value()}, Output: {var[f'output_{t}'][time].solution_value()}")
            else:
                print('No Optimal Solution found.')
