from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Data
marketing_lim = [
    [500, 1000, 300, 300, 800, 200, 100],   # January
    [600, 500, 200, 0, 400, 300, 150],      # February
    [300, 600, 0, 0, 500, 400, 100],        # March
    [200, 300, 400, 500, 200, 0, 100],      # April
    [0, 100, 500, 100, 1000, 300, 0],       # May
    [500, 500, 100, 300, 1100, 500, 60]     # June
]

# machines = [4, 2, 3, 1, 1]
# machines available for each month
n_machines = [
    [3,2,3,1,1],
    [4,2,1,1,1],
    [4,2,3,0,1],
    [4,1,3,1,1],
    [3,1,3,1,1],
    [4,2,2,1,0]
] 
# Time taken by each machine 
time = [
    [0.5, 0.7, 0, 0, 0.3, 0.2, 0.5],  # Grinding
    [0.1, 0.2, 0, 0.3, 0, 0.6, 0],  # Vertical drilling
    [0.2, 0, 0.8, 0, 0, 0, 0.6],  # Horizontal drilling
    [0.05, 0.03, 0, 0.07, 0.1, 0, 0.08],  # Boring
    [0, 0, 0.01, 0, 0.05, 0, 0.05]  # Planing
]
# time = [
#     [0.5, 0.7, float('inf'), float('inf'), 0.3, 0.2, 0.5],  # Grinding
#     [0.1, 0.2, float('inf'), 0.3, float('inf'), 0.6, float('inf')],  # Vertical drilling
#     [0.2, float('inf'), 0.8, float('inf'), float('inf'), float('inf'), 0.6],  # Horizontal drilling
#     [0.05, 0.03, float('inf'), 0.07, 0.1, float('inf'), 0.08],  # Boring
#     [float('inf'), float('inf'), 0.01, float('inf'), 0.05, float('inf'), 0.05]  # Planing
# ]
# Contribution to profit of each machines
profit_cotri = [10, 6, 8, 4, 11, 9, 3]


# Defining the decision variables
sold = {}
hold = {}
produced = {}

months = range(6)
prods = range(7)
machines = range(5)

for month in months:
    # if month == 5:
    #     for prod in prods:
    #         sold[(prod,month)] = solver.IntVar(0,solver.infinity(),f"sold_{prod}_{month}" )
    #         produced[(prod,month)] = solver.IntVar(0,marketing_lim[month][prod],f"produced_{prod}_{month}" )
    # else:
    #     
    for prod in prods:
        sold[(prod,month)] = solver.NumVar(0,solver.infinity(),f"sold_{prod}_{month}" )
        hold[(prod, month)] = solver.NumVar(0,100,f"hold_{prod}_{month}" )
        produced[(prod,month)] = solver.NumVar(0,marketing_lim[month][prod],f"produced_{prod}_{month}" )

# Define the constraints
# Time Constraint
for month in months:
    for machine in machines:
        solver.Add(sum([produced[(prod,month)]*time[machine][prod] for prod in prods]) <= n_machines[month][machine]*24*16)

# Linking constraints
for prod in prods:
    solver.Add(produced[(prod,0)] == hold[(prod,0)] + sold[(prod,0)])

for month in range(1,6):
    for prod in prods:
        solver.Add(produced[(prod,month)] + hold[(prod,month-1)] == hold[(prod,month)] + sold[(prod,month)])

# for prod in prods:
#         solver.Add(produced[(prod,5)] + hold[(prod,4)] == 50 + sold[(prod,5)])
for prod in prods:
    solver.Add(hold[(prod,5)] == 50)

# Set the objective function
profit = solver.Objective()

for month in range(6):
    for prod in prods:
        profit.SetCoefficient(sold[(prod,month)],profit_cotri[prod])
        profit.SetCoefficient(hold[(prod,month)],-0.5)
# for prod in prods:
#     profit.SetCoefficient(sold[(prod,5)],profit_cotri[prod])
#     # profit.SetCoefficient(50,-0.5)
profit.SetMaximization()
status = solver.Solve()

# if status == pywraplp.Solver.OPTIMAL:
#     print('Optimal solution found:')
#     print(f'Optimal profit: {profit.Value()}')
# else:
#     print('The problem does not have an optimal solution.')

# Print the solution in a readable tabular format
if status == pywraplp.Solver.OPTIMAL:
    print('Optimal solution found:')
    print(f'Optimal profit: {profit.Value()}')

    # Print header
    print(f'{"Month":<8}{"Produced":<60}{"Sold":<60}{"Hold":<60}')
    print('-' * 180)

    for month in months:
        produced_str = ' | '.join([f'{produced[(prod, month)].solution_value():<8.0f}' for prod in prods])
        sold_str = ' | '.join([f'{sold[(prod, month)].solution_value():<8.0f}' for prod in prods])
        if month < 5:
            hold_str = ' | '.join([f'{hold[(prod, month)].solution_value():<8.0f}' for prod in prods])
        else:
            hold_str = '-' * 60
        print(f'{month + 1:<8}{produced_str:<60}{sold_str:<60}{hold_str:<60}')

else:
    print('The problem does not have an optimal solution.')