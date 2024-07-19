from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver('SCIP')


# Requirements
requirement = [
    [1000, 1400, 1000],  # Year 1
    [500, 2000, 1500],   # Year 2
    [0, 2500, 2000]        # Year 3
]

# Initial Strength
strength = [2000, 1500, 1000]
# Define the decision variables
current = {}
recruitement = {}
retraining = {}
downgrading = {}
redundancy = {}
short_time_training = {}
overmanning = {}

categories = ['u', 'ss', 's']
down_cats = ['s_ss','s_u','ss_u']
for year in range(1,4):
    for category in categories:
        current[(year,category)] = solver.IntVar(0,solver.infinity(),f"current_{year}_{category}]")
        recruitement[(year, category)] = solver.IntVar(0,solver.infinity(),f"recruitement_{year}_{category}]")
        redundancy[(year, category)] = solver.IntVar(0,solver.infinity(),f"redundancy_{year}_{category}]")
        short_time_training[(year, category)] = solver.IntVar(0,solver.infinity(),f"short_time_working_{year}_{category}]")
        overmanning[(year,category)] = solver.IntVar(0,solver.infinity(),f"overmanning_{year}_{category}]")
    for category in categories[1:]:
        retraining[(year, category)] = solver.IntVar(0,solver.infinity(),f"retraining_{year}_{category}]")
    for category in down_cats:
        downgrading[(year, category)] = solver.IntVar(0,solver.infinity(),f"downgrading_{year}_{category}]")

for category in categories:
        current[(0,category)] = solver.IntVar(0,solver.infinity(),f"current_{0}_{category}]")

# Define constraints

# Initial Strength
for i,category in enumerate(categories):
    solver.Add(current[(0,category)] == strength[i])

# Continuity Constraint
for year in range(1,4):
    solver.Add(current[(year, 's')] == 0.95*current[(year-1, 's')] + 0.9*recruitement[(year,'s')] + 0.95*retraining[(year,'s')] - downgrading[(year,'s_ss')] -downgrading[(year,'s_u')] -redundancy[(year,'s')])
    solver.Add(current[(year, 'ss')] == 0.95*current[(year-1, 'ss')] + 0.8*recruitement[(year,'ss')] + 0.95*retraining[(year, 'ss')] +0.5*downgrading[(year,'s_ss')] -downgrading[(year, 'ss_u')] -redundancy[(year, 'ss')] -retraining[(year,'s')])
    solver.Add(current[(year, 'u')] == 0.9*current[(year-1, 'u')] + 0.75*recruitement[(year, 'u')] + 0.5*downgrading[(year, 'ss_u')] + 0.5*downgrading[(year, 's_u')] -redundancy[(year, 'u')] -retraining[(year,'ss')])

# Retraining constraints
for year in range(1,4):
    solver.Add(retraining[(year,'ss')] <= 200)
    solver.Add(retraining[(year, 's')] <= 0.25*current[(year,'s')])

# Overrmanning Constraint
for year in range(1,4):
    solver.Add(sum([overmanning[(year,category)] for category in categories]) <= 150)

# Requirement Constraint
for year in range(1,4):
    for i,category in enumerate(categories):
        solver.Add(current[(year,category)] - overmanning[(year,category)] - 0.5*short_time_training[(year, category)] == requirement[year-1][i])

# Upper Bound constraint
for year in range(1,4):
    for category in categories:
        solver.Add(short_time_training[(year, category)] <= 50)
    solver.Add(recruitement[(year, 's')] <= 500)
    solver.Add(recruitement[(year, 'ss')] <= 800)
    solver.Add(recruitement[(year, 'u')] <= 500)

# Define the objective function
total_redundancy = solver.Objective()

for year in range(1,4):
    for category in categories:
        total_redundancy.SetCoefficient(redundancy[(year, category)],1)

total_redundancy.SetMinimization()
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('Optimal solution found:')
    print(f'Optimal redundancy: {total_redundancy.Value()}')
else:
    print('The problem does not have an optimal solution.')
