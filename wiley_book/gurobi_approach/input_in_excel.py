import pandas as pd

# Define the data
time_slots = list(range(5))
durations = [6, 3, 6, 3, 6]
types = list(range(3))
availability = [12, 10, 5]
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
demands = [15000, 30000, 25000, 40000, 27000]

# Create dataframes
df_time_slots = pd.DataFrame(time_slots, columns=['time_slots'])
df_durations = pd.DataFrame(durations, columns=['durations'])
df_types = pd.DataFrame(types, columns=['types'])
df_availability = pd.DataFrame(availability, columns=['availability'])
df_demands = pd.DataFrame(demands, columns=['demands'])

# Create a dataframe for power plant data
df_power_plant_data = pd.DataFrame(power_plant_data).transpose()

# Write dataframes to an Excel file
with pd.ExcelWriter('./data/power_plant_data.xlsx') as writer:
    df_time_slots.to_excel(writer, sheet_name='time_slots', index=False)
    df_durations.to_excel(writer, sheet_name='durations', index=False)
    df_types.to_excel(writer, sheet_name='types', index=False)
    df_availability.to_excel(writer, sheet_name='availability', index=False)
    df_demands.to_excel(writer, sheet_name='demands', index=False)
    df_power_plant_data.to_excel(writer, sheet_name='power_plant_data')
