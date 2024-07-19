from ortools.linear_solver import pywraplp

# Create the solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Define the prices for each month
prices = [
    [110, 120, 130, 110, 115],  # January
    [130, 130, 110, 90, 115],   # February
    [110, 140, 130, 100, 95],   # March
    [120, 110, 120, 120, 125],  # April
    [100, 120, 150, 110, 105],  # May
    [90, 100, 140, 80, 135]     # June
]

# Define the hardness of each oil
hardness = [8.8, 6.1, 2.0, 4.2, 5.0]

# Initial stock
initial_stock = 500

# Maximum production capacities
max_veg_production = 200
max_non_veg_production = 250

# Storage cost per ton per month
storage_cost = 5

# Selling price of the final product
selling_price = 150

# Define the decision variables
purchase = {}  # purchase[oil][month]
storage = {}   # storage[oil][month]
used = {}      # used[oil][month]
production = []  # production[month]
is_used = {}

for month in range(6):
    for oil in range(5):
        purchase[(oil, month)] = solver.IntVar(0, solver.infinity(), f'purchase_{oil}_{month}')
        storage[(oil, month)] = solver.IntVar(0, 1000, f'storage_{oil}_{month}')
        used[(oil, month)] = solver.IntVar(0, solver.infinity(), f'used_{oil}_{month}')
        is_used[(oil, month)] = solver.BoolVar(f'is_used_{oil}_{month}')
    production.append(solver.IntVar(0, solver.infinity(), f'production_{month}'))

# Define constraints
# Initial stock constraints
for oil in range(5):
    solver.Add(storage[(oil, 0)] == initial_stock + purchase[(oil, 0)] - used[(oil, 0)])

# Stock balance and storage constraints for subsequent months
for month in range(1, 6):
    for oil in range(5):
        solver.Add(storage[(oil, month)] == storage[(oil, month-1)] + purchase[(oil, month)] - used[(oil, month)])

# Ensure the initial stock exists at the end of June
for oil in range(5):
    solver.Add(storage[(oil, 5)] == initial_stock)

# Production capacity constraints
for month in range(6):
    veg_used = used[(0, month)] + used[(1, month)]
    non_veg_used = used[(2, month)] + used[(3, month)] + used[(4, month)]
    solver.Add(veg_used <= max_veg_production)
    solver.Add(non_veg_used <= max_non_veg_production)

# used or not used constraints
for month in range(6):
    solver.Add(used[(0,month)] <= max_veg_production*is_used[(0,month)])
    solver.Add(used[(1,month)] <= max_veg_production*is_used[(1,month)])
    solver.Add(used[(2,month)] <= max_non_veg_production*is_used[(2,month)])
    solver.Add(used[(3,month)] <= max_non_veg_production*is_used[(3,month)])
    solver.Add(used[(4,month)] <= max_non_veg_production*is_used[(4,month)])

# Atleast 20 constraint
for month in range(6):
    for oil in range(5):
        solver.Add(used[(oil, month)] >= 20*is_used[(oil, month)])

# veg1 veg2 oil3 constraint
for month in range(6):
    solver.Add(is_used[(0, month)] + is_used[(1, month)] <= 2*is_used[(4, month)])
# Hardness constraints
for month in range(6):
    hardness_constraint = sum(hardness[oil] * used[(oil, month)] for oil in range(5))
    solver.Add(hardness_constraint >= 3*production[month])
    solver.Add(hardness_constraint <= 6*production[month])

# Production equals the sum of used oils for each month
for month in range(6):
    solver.Add(production[month] == sum(used[(oil, month)] for oil in range(5)))

# Maximum three oils constraint
for month in range(6):
    solver.Add(sum(is_used[(oil, month)] for oil in range(5)) <= 3)

# Define the objective function
profit = solver.Objective()
for month in range(6):
    for oil in range(5):
        profit.SetCoefficient(purchase[(oil, month)], -prices[month][oil])
        profit.SetCoefficient(storage[(oil, month)], -storage_cost)
    profit.SetCoefficient(production[month], selling_price)
profit.SetMaximization()

# Solve the problem
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('Optimal solution found:')
    print(f'Optimal profit: {profit.Value()}')

    # Print header
    print('\nMonth  |  Purchase (tons)          |  Storage (tons)            |  Used (tons)               |  Production (tons)')
    print('-' * 150)

    for month in range(6):
        # Initialize empty lists for each column
        purchases = []
        storages = []
        used_oils = []

        # Collect data for each oil type
        for oil in range(5):
            purchases.append(f'{purchase[(oil, month)].solution_value():<28}')
            storages.append(f'{storage[(oil, month)].solution_value():<28}')
            used_oils.append(f'{used[(oil, month)].solution_value():<28}')

        # Print data for the current month
        print(f'{month + 1:<6} |  ' + '  |  '.join(purchases) + '  |  ' + '  |  '.join(storages) + '  |  ' + '  |  '.join(used_oils) + f'  |  {production[month].solution_value():<22}')
        print("-"*150)
else:
    print('The problem does not have an optimal solution.')