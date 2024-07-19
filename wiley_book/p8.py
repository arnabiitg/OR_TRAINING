from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver('SCIP')

# Data
mines = range(4)
years = range(5)
royalty = [[] for _ in years]
royalty[0] = [5,4,4,5]
quality = [1,0.7,1.5,0.5]
yearly_requirement = [0.9,0.8,1.2,0.6,1]
extraction_lim = [2,2.5,1.3,3]
selling_price = [10]

for year in years[1:]:
    royalty[year] = [royalty[year-1][mine]*0.9 for mine in  mines]
    selling_price.append(selling_price[-1]*0.9)

# Decision Variables
mine_open = [[solver.BoolVar(f'open_{mine}_{year}') for mine in mines] for year in years]
mine_oper = [[solver.BoolVar(f'oper_{mine}_{year}') for mine in mines] for year in years]
extraction = [[solver.NumVar(0,solver.Infinity(),f'oper_{mine}_{year}') for mine in mines] for year in years]
blended_ore = [solver.NumVar(0,solver.Infinity(), f'blended_ore_{year}') for year in years]
# revenue = [solver.NumVar(0,solver.Infinity(), f'revenue_{year}') for year in years]
expenditure = [solver.NumVar(0,solver.Infinity(), f'expenditure_{year}') for year in years]

# Constraints
# Mine opening Constraint
for year in years:
    for mine in mines:
        solver.Add(mine_oper[year][mine] <= mine_open[year][mine])
for year in years[1:]:
    for mine in mines:
        solver.Add(mine_open[year][mine] <= mine_open[year-1][mine])
# Mine operating Constraint
for year in years:
    solver.Add(sum([mine_oper[year][mine] for mine in mines]) <= 3)

# Extraction Constraint
for year in years:
    for mine in mines:
        solver.Add(extraction[year][mine] <=  mine_oper[year][mine]*extraction_lim[mine]*1000000)

# Ore equality
for year in years:
    solver.Add(sum([extraction[year][mine] for mine in mines]) == blended_ore[year])
# Quality Constraint
for year in years:
    solver.Add(sum([extraction[year][mine]*quality[mine] for mine in mines]) == yearly_requirement[year]*blended_ore[year])
# Revenue calculation constraint
for year in years:
    # solver.Add(revenue[year] == sum([extraction[year][mine]*selling_price[year] for mine in mines]))
    solver.Add(expenditure[year] == sum([mine_open[year][mine]*royalty[year][mine]*1000000 for mine in mines]))

# for year in years[1:]:
#     solver.Add(revenue[year] == 0.9*revenue[year-1])
#     solver.Add(expenditure[year] == 0.9*expenditure[year-1])

profit = solver.Objective()
for year in years:
    profit.SetCoefficient(blended_ore[year], selling_price[year])
    profit.SetCoefficient(expenditure[year], -1)

profit.SetMaximization()
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('Optimal solution found:')
    print(f'Optimal profit: {profit.Value()}')
    for year in years:
        print(f"Year {year}:")
        for mine in mines:
            print(f"Mine_{mine} is: ",mine_oper[year][mine].solution_value())
            print(f"Extracted Amount of Mine {mine}: ", extraction[year][mine].solution_value())

        print('*'*100)

else:
    print('The problem does not have an optimal solution.')

