class Read:
    def __init__(self, id) :
        self.id = id
    def read_data(self):
        data = {}
        if self.id == 15:
            # Define the time slots and durations
            time_slots = range(5)
            durations = [6, 3, 6, 3, 6]

            # Define the types of power plants and their availability
            types = range(3)
            availability = [12, 10, 5]

            # Define the power plant data
            power_plant_data = {
                0: {
                    "Minimum_level_(MW)": 850,
                    "Maximum_level_(MW)": 2000,
                    "Cost_per_hour_at_minimum": 1000,
                    "Cost_per_hour_per_megawatt_above_minimum": 2,
                    "Fixed_cost": 2000
                },
                1: {
                    "Minimum_level_(MW)": 1250,
                    "Maximum_level_(MW)": 1750,
                    "Cost_per_hour_at_minimum": 2600,
                    "Cost_per_hour_per_megawatt_above_minimum": 1.30,
                    "Fixed_cost": 1000
                },
                2: {
                    "Minimum_level_(MW)": 1500,
                    "Maximum_level_(MW)": 4000,
                    "Cost_per_hour_at_minimum": 3000,
                    "Cost_per_hour_per_megawatt_above_minimum": 3,
                    "Fixed_cost": 500
                }
            }

            # Define the demand in each time slot (in megawatts)
            demands = [15000, 30000, 25000, 40000, 27000] # In megawatts

            data['time_slots'] = time_slots
            data['types'] = types
            for time in time_slots:
                data[f'demands[{time}]'] = demands[time]

            for type in types:
                data[f'durations[{type}]'] = durations[type]
                data[f'availability[{type}]'] = availability[type]
                data[f'power_plant_data[{type}]'] = power_plant_data[type]
        return data