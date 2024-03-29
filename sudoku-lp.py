import sys
import math
from sys import argv
from gurobipy import *
from datetime import datetime

def read_sudoku_file(file_name):
    with open(file_name,"r") as file:
        content = file.readlines()
        sudoku = []
        for line in content:
            row = [int(n) for n in line.split()]
            sudoku.append(row)
    return sudoku


def main():
    if len(argv) < 3:
        print "First argument: file name.argument"
        print "Second argument: sudoku dimension"
        return 1


    dim = int(argv[1])
    file_name = argv[2]
    sudoku = read_sudoku_file(file_name)
    #display(sudoku,n,file)
    file = open(file_name+".output","w")


    model = Model('sudoku')

    #VARIABLES
    vars = {}
    for i in range(dim**2):
        for j in range(dim**2):
            for k in range(dim**2):
                vars[i,j,k] = model.addVar(vtype=GRB.BINARY, name='X_'+ str(i)+'_'+str(j)+'_'+str(k))
    model.update()

    #FIXED POSITIONS RESTRICTION
    for i in range(dim**2):
        for j in range(dim**2):
            if sudoku[i][j] != 0:
                k = int(sudoku[i][j]) - 1
                model.addConstr(vars[i,j,k] == 1, 'F_' + str(i) + '_' + str(j))

    #POSITIONS RESTRICTION#
    for i in range(dim**2):
        for j in range(dim**2):
            model.addConstr(quicksum([vars[i,j,k] for k in range(dim**2)]) == 1, 'P_' + str(i) + '_' + str(j))

    #ROWS RESTRICTION
    for i in range(dim**2):
        for k in range(dim**2):
            model.addConstr(quicksum([vars[i,j,k] for j in range(dim**2)]) == 1, 'R_' + str(i) + '_' + str(k))

    #COLUMNS RESTRICTION
    for j in range(dim**2):
        for k in range(dim**2):
            model.addConstr(quicksum([vars[i,j,k] for i in range(dim**2)]) == 1, 'C_' + str(j) + '_' + str(k))

    #BLOCKS RESTRICTION
    for k in range(dim**2):
        for m in range(dim):
            for n in range(dim):
                subgrid = [vars[i,j,k] for i in range(m*dim, (m+1)*dim)
                    for j in range(n*dim, (n+1)*dim)]
                model.addConstr(quicksum(subgrid) == 1, 'B_' + str(m) + '_' + str(n) + '_' + str(k))


    model.optimize()

    model.write(file_name+".lp")

    solution = model.getAttr('X', vars)

    for i in range(dim**2):
        sol = ''
        for j in range(dim**2):
            for k in range(dim**2):
                if solution[i,j,k] > 0.5:
                    if(n>=10):
                        sol += "%03d " % (k+1)
                    elif(n>=4):
                        sol += "%02d " % (k+1)
                    else:
                        sol += "%d " % (k+1)
        file.write(sol+"\n")

    return 0

if __name__ == "__main__":
    main()
