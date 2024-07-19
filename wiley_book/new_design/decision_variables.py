class input:
    def __init__(self, id) :
        self.id = id
    def create_variables(self, solver, data):
        var = {}
        if self.id == 9:
            years = range(6)
            industries = ['coal','steel','transport']
            var['coal_stocked'] = [solver.NumVar(0,solver.infinity(),f'coal_stocked_{year}') for year in years]
            var['steel_stocked'] = [solver.NumVar(0,solver.infinity(),f'steel_stocked_{year}') for year in years]
            var['transport_stocked'] = [solver.NumVar(0,solver.infinity(),f'steel_stocked_{year}') for year in years]
            var['coal_prod'] = [solver.NumVar(0,solver.infinity(),f'coal_produced_{year}') for year in years]
            var['steel_prod'] = [solver.NumVar(0,solver.infinity(),f'steel_produced_{year}') for year in years]
            var['transport_prod'] = [solver.NumVar(0,solver.infinity(),f'transport_produced_{year}') for year in years]
            var['extra_cap'] = {
                'coal' : [solver.NumVar(0,solver.infinity(),f'capacity_{year}_coal') for year in years],
                'steel' : [solver.NumVar(0,solver.infinity(),f'capacity_{year}_steel') for year in years],
                'transport' : [solver.NumVar(0,solver.infinity(),f'capacity_{year}_transport') for year in years]
            }
        elif self.id == 11:
            points = {
                'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0],
                'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3]
            }

            var['z'] = [solver.NumVar(0,solver.infinity(),f'z_{i}') for i in range(len(points['x']))] 
            var['a'] = [solver.NumVar(0,solver.infinity(),f'a_{i}') for i in range(len(points['x']))]
            var['b'] = [solver.NumVar(0,solver.infinity(),f'b_{i}') for i in range(len(points['x']))]
            
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
            for retailer in retailers:
                var[f'c_{retailer}_D1'] = solver.BoolVar(f'c_{retailer}_D1')
            # var[f'c_{retailer}_D2'] = solver.BoolVar(f'c_{retailer}_D2')

            # Define deviation variables
            var['delivery_break'] = solver.NumVar(0, 0.05, 'delivery_break')
            var['spirit_break'] = solver.NumVar(0, 0.05, 'spirit_break')
            for region in regions:
                var[f'oil_{region}_break'] = solver.NumVar(0, 0.05, f'oil_{region}_break')
            for category in categories:
                var[f'group_break_{category}'] = solver.NumVar(0, 0.05, f'group_break_{category}')

        elif self.id == 15:
            for t in data['types']:
                var[f'active_{t}'] = [solver.NumVar(0, data[f'availability[{t}]'], f'active_{t}_{time}') for time in data['time_slots']]
                var[f'started_{t}'] = [solver.NumVar(0, data[f'availability[{t}]'], f'started_{t}_{time}') for time in data['time_slots']]
                var[f'output_{t}'] = [solver.NumVar(0, solver.infinity(), f'output_{t}_{time}') for time in data['time_slots']]
        return var



