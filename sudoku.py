import sys
import math
from gurobipy import *

def display(sudoku,dim):
    for row in sudoku:
        if dim > 3:
            print " ".join("%02d" % x for x in sudoku)
        else:
            print " ".join(str(x) for x in row)
    print "\n"

def read_sudoku_file(file_name,dim,sudoku):
    with open(file_name,"r") as file:
        content = file.readlines()
        for line in content:
            row = [int(n) for n in line.split()]
            sudoku.append(row)

d = 10
dim = d**2
sudoku = []
read_sudoku_file("size10",dim,sudoku)

vars = {}

model = Model('sudoku')

for i in range(dim):
    for j in range(dim):
        for v in range(dim):
            vars[i,j,v] = model.addVar(vtype=GRB.BINARY, name='G_'+ str(i)+'_'+str(j)+'_'+str(v))
                 
model.update()

for i in range(dim):
    for j in range(dim):
        if sudoku[i][j] != 0:
            v = int(sudoku[i][j]) - 1
            model.addConstr(vars[i,j,v] == 1, 'Fix_' + str(i) + '_' + str(j))

for i in range(dim):
    for j in range(dim):
        model.addConstr(quicksum([vars[i,j,v] for v in range(dim)]) == 1, 'V_' + str(i) + '_' + str(j))
                 
for i in range(dim):
    for v in range(dim):
        model.addConstr(quicksum([vars[i,j,v] for j in range(dim)]) == 1, 'R_' + str(i) + '_' + str(v))

for j in range(dim):
    for v in range(dim):
        model.addConstr(quicksum([vars[i,j,v] for i in range(dim)]) == 1, 'C_' + str(j) + '_' + str(v))

for v in range(dim):
    for i0 in range(d):
        for j0 in range(d):
            subgrid = [vars[i,j,v] for i in range(i0*d, (i0+1)*d)
                for j in range(j0*d, (j0+1)*d)]
            model.addConstr(quicksum(subgrid) == 1, 'Sub_' + str(i0) + '_' + str(j0) + '_' + str(v))

model.optimize()

model.write('sudoku.lp')

print('')
print('Solution:')
print('')

# Retrieve optimization result

solution = model.getAttr('X', vars)

for i in range(dim):
    sol = ''
    for j in range(dim):
        for v in range(dim):
            if solution[i,j,v] > 0.5:
                sol += str(v+1)
    print(sol)