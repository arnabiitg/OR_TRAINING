class Constraints:
    def __init__(self, id):
        self.id = id
    def add_const(self,solver, var, data):
        # Data
        # Create the 2D dictionary
        if self.id == 9:
            initial_cap = {
                'coal' : 300,
                'steel' : 350,
                'transport' : 280
            }
            prod = {
                'coal': {
                    'coal': 0.0,
                    'steel': 0.7,
                    'transport': 0.9,
                    'manpower': 0.4
                },
                'steel': {
                    'coal': 0.1,
                    'steel': 0.1,
                    'transport': 0.2,
                    'manpower': 0.2
                },
                'transport': {
                    'coal': 0.2,
                    'steel': 0.1,
                    'transport': 0.2,
                    'manpower': 0.1
                }
            }
            cap_inc = {
                'coal': {
                    'coal': 0.1,
                    'steel': 0.5,
                    'transport': 0.4,
                    'manpower': 0.6
                },
                'steel': {
                    'coal': 0.1,
                    'steel': 0.1,
                    'transport': 0.2,
                    'manpower': 0.3
                },
                'transport': {
                    'coal': 0.2,
                    'steel': 0.1,
                    'transport': 0.2,
                    'manpower': 0.2
                }
            }
            init_stock = {'coal': 150, 'steel': 80, 'transport': 100}
            ex = {'coal': 60, 'steel': 60, 'transport': 30}
            years = range(1,6)
            industries = ['coal','steel','transport']

            # Linking Constraints
            for year in range(1,6):
                if year == 1:
                    for industry in industries:
                        solver.Add(init_stock[industry] + var[f'{industry}_prod'][year] 
                                == ex[industry] + var[f'{industry}_stocked'][year])
                else:
                    for industry in industries:
                        solver.Add(var[f'{industry}_stocked'][year-1] + var[f'{industry}_prod'][year] 
                                == ex[industry] + var[f'{industry}_stocked'][year])
            
            # Future Use Constraints
            for year in range(4):
                if year == 0:
                    for industry in industries:
                        solver.Add(init_stock[industry] >= sum(var[f'{ind}_prod'][year+1]*prod[ind][industry] for ind in industries)
                                    + sum(var['extra_cap'][industry][year+2]*cap_inc[industry][ind] for ind in industries))
                else:
                    for industry in industries:
                        solver.Add(var[f'{industry}_stocked'][year] >= sum(var[f'{ind}_prod'][year+1]*prod[ind][industry] for ind in industries)
                                    + sum(var['extra_cap'][industry][year+2]*cap_inc[industry][ind] for ind in industries))
                        
            # Capacity Constraints
            for year in years:
                for industry in industries:
                    solver.Add(var[f'{industry}_prod'][year] <= initial_cap[industry] + sum(var['extra_cap'][industry][y] for y in range(1,year)))


            # Manpower Constraint
            for year in range(2,6):
                solver.Add(sum(var['extra_cap'][industry][year]*cap_inc[industry]['manpower'] for industry in industries) 
                           + sum(var[f'{industry}_prod'][year]*prod[industry]['manpower'] for industry in industries) <= 470)
                
        elif self.id == 11:
            points = {
                'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0],
                'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3]
            }

            # Absolute Value Constraints
            for i in range(len(points['x'])):
                solver.Add(var['z'][i] >= points['y'][i] - (var['a'][i]*points['x'][i] + var['b'][i]))
                solver.Add(var['z'][i] >= -points['y'][i] + (var['a'][i]*points['x'][i] + var['b'][i]))

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

            # Calculate total values
            total_delivery = sum(data[retailer]["Delivery_points"] for retailer in retailers)
            total_spirit = sum(data[retailer]["Spirit_market"] for retailer in retailers)
            total_oil = {region: sum(data[retailer]["Oil_market"] for retailer in retailers if data[retailer]["Region"] == region) for region in regions}
            total_retailers = {category: sum(1 for retailer in retailers if data[retailer]["Growth_category"] == category) for category in categories}

            # Splitting Constraints
            # Total Number of Delivery Points Splitting
            delivery_d1 = sum(var[f'c_{retailer}_D1'] * data[retailer]["Delivery_points"] for retailer in retailers)
            solver.Add(delivery_d1 <= 0.45 * total_delivery)
            solver.Add(delivery_d1 >= 0.35 * total_delivery)
            solver.Add(var['delivery_break'] >= (delivery_d1 / total_delivery) - 0.40)
            solver.Add(var['delivery_break'] >= -(delivery_d1 / total_delivery) + 0.40)

            # Spirit Market Splitting
            spirit_d1 = sum(var[f'c_{retailer}_D1'] * data[retailer]["Spirit_market"] for retailer in retailers)
            solver.Add(spirit_d1 <= 0.45 * total_spirit)
            solver.Add(spirit_d1 >= 0.35 * total_spirit)
            solver.Add(var['spirit_break'] >= (spirit_d1 / total_spirit) - 0.40)
            solver.Add(var['spirit_break'] >= -(spirit_d1 / total_spirit) + 0.40)

            # Oil Market Splitting by Region
            for region in regions:
                oil_d1 = sum(var[f'c_{retailer}_D1'] * data[retailer]["Oil_market"] for retailer in retailers if data[retailer]["Region"] == region)
                solver.Add(oil_d1 <= 0.45 * total_oil[region])
                solver.Add(oil_d1 >= 0.35 * total_oil[region])
                solver.Add(var[f'oil_{region}_break'] >= (oil_d1 / total_oil[region]) - 0.40)
                solver.Add(var[f'oil_{region}_break'] >= -(oil_d1 / total_oil[region]) + 0.40)

            # Retailer Splitting by Growth Category
            for category in categories:
                n_retailer_d1 = sum(var[f'c_{retailer}_D1'] for retailer in retailers if data[retailer]['Growth_category'] == category)
                solver.Add(n_retailer_d1 <= 0.45 * total_retailers[category])
                solver.Add(n_retailer_d1 >= 0.35 * total_retailers[category])
                solver.Add(var[f'group_break_{category}'] >= (n_retailer_d1 / total_retailers[category]) - 0.40)
                solver.Add(var[f'group_break_{category}'] >= -(n_retailer_d1 / total_retailers[category]) + 0.40)
        
        elif self.id == 15:
            # Starting Constraint
            for time in data['time_slots']:
                if time == 0:
                    for type in data['types']:
                        solver.Add(var[f'started_{type}'][time] >= var[f'active_{type}'][time])
                else:
                    for type in data['types']:
                        solver.Add(var[f'started_{type}'][time] >= var[f'active_{type}'][time] - var[f'active_{type}'][time-1])
            # Output Constraints
            for time in data['time_slots']:
                for t in data['types']:
                    solver.Add(var[f'output_{t}'][time] >= var[f'active_{t}'][time] * data[f'power_plant_data[{t}]']["Minimum_level_(MW)"])
                    solver.Add(var[f'output_{t}'][time] <= var[f'active_{t}'][time] * data[f'power_plant_data[{t}]']["Maximum_level_(MW)"])

            # Demand Constraints with 15% reserve
            for time in data['time_slots']:
                solver.Add(sum(var[f'output_{t}'][time] for t in data['types']) == data[f'demands[{time}]'])
                solver.Add(sum(var[f'active_{t}'][time] * data[f'power_plant_data[{t}]']['Maximum_level_(MW)'] for t in data['types']) >= 1.15 * data[f'demands[{time}]'])
            

                           