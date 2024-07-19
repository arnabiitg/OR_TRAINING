from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver('SCIP')

# Data
max_labour_hour = 5500
years = range(5)
ages = range(13)
grain_types = range(4)
grain_production = [1.1,0.9,0.8,0.65]
grain_limit = [20,30,20,10]
labour = {'heifer':10, 'milk_cow':42, 'grain': 4, 'sugar': 14}

# Decision Variables
milk_cows = [[solver.NumVar(0,solver.infinity(),f'milk_cows_{year}_{age}') for age in range(3,13)] for year in years]
heifers = [[solver.NumVar(0,solver.infinity(),f'heifers_{year}_{age}') for age in range(3)] for year in years]
acre_for_grain = [[solver.NumVar(0,solver.infinity(),f'acre_for_grain_{year}_{type}') for type in grain_types] for year in years]
acre_for_sugar = [solver.NumVar(0,solver.infinity(),f'sugar_acres_{year}') for year in years]
grain_produced = [[solver.NumVar(0,solver.infinity(),f'grain_produced_{year}_{type}') for type in grain_types] for year in years]
sugar_produced = [solver.NumVar(0,solver.infinity(),f'sugar_produced_{year}') for year in years]
heifers_sold = [solver.NumVar(0,solver.infinity(),f'heifers_sold_{year}') for year in years]
extra_hours = [solver.NumVar(0,solver.infinity(),f'extra_hours_{year}') for year in years]
grain_bought = [solver.NumVar(0,solver.infinity(),f'grain_bought_{year}') for year in years]
sugar_bought = [solver.NumVar(0,solver.infinity(),f'sugar_bought_{year}') for year in years]
grain_sold = [solver.NumVar(0,solver.infinity(),f'grain_sold_{year}') for year in years]
sugar_sold = [solver.NumVar(0,solver.infinity(),f'sugar_sold_{year}') for year in years]


# Constraints
for year in years:

    # Crop linking Constraints
    sugar_used = sum([milk_cows[year][age] for age in range(2,13)]*0.7)
    grain_used = sum([milk_cows[year][age] for age in range(2,13)]*0.6)
    solver.Add(sugar_bought[year] + sugar_produced[year] == sugar_sold[year] + sugar_used)
    solver.Add(grain_bought[year] + sum(grain_produced[year][type] for type in grain_types) 
               == grain_sold[year] + grain_used)
    # Capacity Constraints
    solver.Add(sum([heifers[year][age] for age in range(3)])
                + sum([milk_cows[year][age] for age in range(2,13)]) <= 200)
    # Linking Constraints
    if year == 0:
        solver.Add(heifers[year][1] == 10)   # Watch out
        solver.Add(heifers[year][2] == 10)
    solver.Add(heifers[year][1] == heifers[year-1][0] - heifers_sold[year-1])   # Watch out
    solver.Add(heifers[year][2] == heifers[year-1][1])   # Watch out

    solver.Add(milk_cows[year][3] == heifers[year][2])   # Watch out

    for age in range(4,13):
        if year == 0:
            solver.Add(milk_cows[year][age] == 10)
        solver.Add(milk_cows[year][age] == milk_cows[year-1][age-1])   # Watch out

    # Newborn Constraints
    solver.Add(heifers[year][0] == sum([milk_cows[year][age] for age in ages]))*1.1

    # # Crop requirement constraints
    # solver.Add(sum([milk_cows[year][age]*0.6 for age in ages]))
    # Crop producing Constraints
    solver.Add(sugar_produced == 1.5*acre_for_sugar)
    for type in grain_types:
        solver.Add(acre_for_grain[year][type] <= grain_limit[type]) 
        solver.Add(grain_produced[year][type] == acre_for_grain[year][type]*grain_production[type])
    
    solver.Add(sum([acre_for_grain[year][type] for type in grain_types]) + acre_for_sugar[year] + 
               (2/3)*sum(heifers[year][age] for age in range(3))
                + sum(milk_cows[year][age] for age in range(2,13)) <= 200)
    
    # Labour constraints
    total_labour_requirement = (sum([heifers[year][age] for age in range(3)])*10 +
                                sum([milk_cows[year][age] for age in ages])*42 
                                + acre_for_sugar[year]*14
                                + sum([acre_for_grain[year][type] for type in grain_types])*labour['grain']
                                )
    solver.Add(total_labour_requirement <= max_labour_hour + extra_hours[year])


    
