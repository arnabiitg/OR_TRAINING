from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver('SCIP')
solver.EnableOutput()

# Data
octane = {'LN':90, 'MN':80, 'HN':70, 'RG': 115, 'CG': 105}
crude_composition = {
    "Crude 1": [0.1, 0.2, 0.2, 0.12, 0.2, 0.13],
    "Crude 2": [0.15, 0.25, 0.18, 0.08, 0.19, 0.12]
}
profit_contri = [700, 600, 400, 350, 150]

# Decision Variables
C_1 = solver.IntVar(0, solver.Infinity(), 'C_1') # Crude 1
C_2 = solver.IntVar(0, solver.Infinity(), 'C_2') # Crude 2
LN = solver.IntVar(0, solver.Infinity(), 'LN') # Light naphtha
LN_RP = solver.IntVar(0, solver.Infinity(), 'LN_RP') # Light naphtha used to make regular petrol
LN_PP = solver.IntVar(0, solver.Infinity(), 'LN_PP') # Light naphtha used to make premium petrol
LN_RG = solver.IntVar(0, solver.Infinity(), 'LN_RG') # Light naphtha used to make reformed gasoline
MN = solver.IntVar(0, solver.Infinity(), 'MN') # Medium naphtha
MN_RP = solver.IntVar(0, solver.Infinity(), 'MN_RP') # Medium naphtha used to make regular petrol 
MN_PP = solver.IntVar(0, solver.Infinity(), 'MN_PP') # Medium naphtha used to make premium petrol
MN_RG = solver.IntVar(0, solver.Infinity(), 'MN_RG') # Medium naphtha used to make reformed gasoline
HN = solver.IntVar(0, solver.Infinity(), 'HN') # Heavy naphtha
HN_RP = solver.IntVar(0, solver.Infinity(), 'HN_RP') # Heavy naphtha used to make regular petrol
HN_PP = solver.IntVar(0, solver.Infinity(), 'HN_PP') # Heavy naphtha used to make premium petrol
HN_RG = solver.IntVar(0, solver.Infinity(), 'HN_RG') # Heavy naphtha used to make reformed gasoline
RG = solver.IntVar(0, solver.Infinity(), 'RG') # Reformed gasoline
RG_RP = solver.IntVar(0, solver.Infinity(), 'RG_RP') # Reformed gasoline used to make regular petrol
RG_PP = solver.IntVar(0, solver.Infinity(), 'RG_PP') # Reformed gasoline used to make premium petrol
LO = solver.IntVar(0, solver.Infinity(), 'LO') # Light oil
LO_JF = solver.IntVar(0, solver.Infinity(), 'LO_JF') # Light oil used to make jet fuel
LO_FO = solver.IntVar(0, solver.Infinity(), 'LO_FO') # Light oil used to make fuel oil
LO_CO = solver.IntVar(0, solver.Infinity(), 'LO_CO') # Light oil used to make cracked oil
LO_CG = solver.IntVar(0, solver.Infinity(), 'LO_CG') # Light oil used to make cracked gasoline
HO = solver.IntVar(0, solver.Infinity(), 'HO') # Heavy oil
HO_JF = solver.IntVar(0, solver.Infinity(), 'HO_JF') # Heavy oil used to make jet fuel
HO_FO = solver.IntVar(0, solver.Infinity(), 'HO_FO') # Heavy oil used to make fuel oil
HO_CO = solver.IntVar(0, solver.Infinity(), 'HO_CO') # Heavy oil used to make cracked oil
HO_CG = solver.IntVar(0, solver.Infinity(), 'HO_CG') # Heavy oil used to make cracked gasoline
CO = solver.IntVar(0, solver.Infinity(), 'CO') # Cracked oil
CO_FO = solver.IntVar(0, solver.Infinity(), 'CO_FO') # Cracked oil used to make fuel oil
CO_JF = solver.IntVar(0, solver.Infinity(), 'CO_JF') # Cracked oil used to make jet fuel
CG = solver.IntVar(0, solver.Infinity(), 'CG') # Cracked gasoline
CG_RP = solver.IntVar(0, solver.Infinity(), 'CG_RP') # Cracked gasoline used to make regular petrol
CG_PP = solver.IntVar(0, solver.Infinity(), 'CG_PP') # Cracked gasoline used to make premium petrol
R = solver.IntVar(0, solver.Infinity(), 'R') # Residuum
R_LBO = solver.IntVar(0, solver.Infinity(), 'R_LBO') # Residuum used to make lube oil
R_JF = solver.IntVar(0, solver.Infinity(), 'R_JF') # Residuum used to make jet fuel
R_FO = solver.IntVar(0, solver.Infinity(), 'R_FO') # Residuum used to make fuel oil
PP = solver.IntVar(0, solver.Infinity(), 'PP') # Premium petrol
RP = solver.IntVar(0, solver.Infinity(), 'RP') # Regular petrol
JF = solver.IntVar(0, solver.Infinity(), 'JF') # Jet fuel
FO = solver.IntVar(0, solver.Infinity(), 'FO') # Fuel oil
LBO = solver.IntVar(0, solver.Infinity(), 'LBO') # Lube oil


pri_el = [LN, MN, HN, LO, HO, R]


# Constraints
# Equality Constraints
solver.Add(LN == LN_RP + LN_PP + LN_RG)
solver.Add(MN == MN_PP +MN_RP +MN_RG)
solver.Add(HN == HN_PP + HN_RP + HN_RG)
solver.Add(RG == RG_PP + RG_RP)
solver.Add(LO == LO_CG + LO_CO + LO_FO + LO_JF)
solver.Add(HO == HO_CG +HO_CO +HO_FO +HO_JF)
solver.Add(CO == CO_FO + CO_JF)
solver.Add(CG == CG_PP + CG_RP)
solver.Add(R == R_JF + R_LBO)

# Blending Constraints
solver.Add(LN == C_1*crude_composition['Crude 1'][0] + C_2*crude_composition['Crude 2'][0])
solver.Add(MN == C_1*crude_composition['Crude 1'][1] + C_2*crude_composition['Crude 2'][1])
solver.Add(HN == C_1*crude_composition['Crude 1'][2] + C_2*crude_composition['Crude 2'][2])
solver.Add(LO == C_1*crude_composition['Crude 1'][3] + C_2*crude_composition['Crude 2'][3])
solver.Add(HO == C_1*crude_composition['Crude 1'][4] + C_2*crude_composition['Crude 2'][4])
solver.Add(R == C_1*crude_composition['Crude 1'][5] + C_2*crude_composition['Crude 2'][5])

solver.Add(RG == 0.6*LN_RG + 0.52*MN_RG + 0.45*HN_RG)
solver.Add(CO == 0.68*LO_CO + 0.75*HO_CO)
solver.Add(CG == 0.28*LO_CG + 0.2*HO_CG)

solver.Add(84*RP <= octane['LN']*LN_RP + octane['HN']*HN_RP + octane['MN']*MN_RP + octane['CG']*CG_RP + octane['RG']*RG_RP)
solver.Add(94*PP <= octane['LN']*LN_PP + octane['HN']*HN_PP + octane['MN']*MN_PP + octane['CG']*CG_PP + octane['RG']*RG_PP) 

solver.Add(JF >= LO_JF + HO_JF*0.6 + CO_JF*1.5 + R_JF*0.05)
solver.Add(JF == LO_JF + HO_JF + CO_JF + R_JF)
solver.Add(PP == LN_PP + MN_PP + HN_PP + RG_PP + CG_PP)
solver.Add(RP == LN_RP + MN_RP + HN_RP + RG_RP + CG_RP)
solver.Add(LO_FO == (10/18)*FO)
solver.Add(CO_FO == (4/18)*FO)
solver.Add(HO_FO == (3/18)*FO)
solver.Add(R_FO == (1/18)*FO)
solver.Add(LBO == 0.5*R_LBO)

solver.Add(C_1 <= 20000)
solver.Add(C_2 <= 30000)
solver.Add(C_1 + C_2 <= 45000)
solver.Add(LN_RG + MN_RG + HN_RG <= 10000)
solver.Add(LO_CO + HO_CO <= 8000)
solver.Add(LBO <= 1000)
solver.Add(LBO >= 500)
solver.Add(PP >= 0.4*RP)

profit  = solver.Objective()

profit.SetCoefficient(PP, 7)
profit.SetCoefficient(RP, 6)
profit.SetCoefficient(JF, 4)
profit.SetCoefficient(FO, 3.5)
profit.SetCoefficient(LBO, 1.5)

profit.SetMaximization()

status = solver.Solve()


# Check the solution status
if status == pywraplp.Solver.OPTIMAL:
    print('Optimal solution found:')
    print(f'Optimal profit: {profit.Value()}')
    print(f'C_1: {C_1.solution_value()}')
    print(f'C_2: {C_2.solution_value()}')
    print(f'LN: {LN.solution_value()}')
    print(f'MN: {MN.solution_value()}')
    print(f'HN: {HN.solution_value()}')
    print(f'RG: {RG.solution_value()}')
    print(f'LO: {LO.solution_value()}')
    print(f'HO: {HO.solution_value()}')
    print(f'CO: {CO.solution_value()}')
    print(f'CG: {CG.solution_value()}')
    print(f'R: {R.solution_value()}')
    print(f'PP: {PP.solution_value()}')
    print(f'RP: {RP.solution_value()}')
    print(f'JF: {JF.solution_value()}')
    print(f'FO: {FO.solution_value()}')
    print(f'LBO: {LBO.solution_value()}')
else:
    print('The problem does not have an optimal solution.')
