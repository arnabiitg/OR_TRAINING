import pandas as pd

class input:
    def read_input(self):
        # Read data from the Excel file
        input_file = "./data/power_plant_data.xlsx"
        df_time_slots = pd.read_excel(input_file, sheet_name='time_slots')
        df_durations = pd.read_excel(input_file, sheet_name='durations')
        df_types = pd.read_excel(input_file, sheet_name='types')
        df_availability = pd.read_excel(input_file, sheet_name='availability')
        df_demands = pd.read_excel(input_file, sheet_name='demands')
        df_power_plant_data = pd.read_excel(input_file, sheet_name='power_plant_data', index_col=0)

        # Convert dataframes back to the appropriate format
        time_slots = df_time_slots['time_slots'].tolist()
        durations = df_durations['durations'].tolist()
        types = df_types['types'].tolist()
        availability = df_availability['availability'].tolist()
        demands = df_demands['demands'].tolist()
        power_plant_data = df_power_plant_data.to_dict(orient='index')

        # Populate the data dictionary
        data = {
            'time_slots': time_slots,
            'types': types
        }
        for time in time_slots:
            data[f'demands[{time}]'] = demands[time]

        for t in types:
            data[f'durations[{t}]'] = durations[t]
            data[f'availability[{t}]'] = availability[t]
            data[f'power_plant_data[{t}]'] = power_plant_data[t]
        
        return data
