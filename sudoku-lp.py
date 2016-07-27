import sys
import math
from sys import argv
from gurobipy import *
from datetime import datetime

def read_sudoku_file(file_name,dim):
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


    n = int(argv[1])
    file_name = argv[2]
    d = n**2
    sudoku = read_sudoku_file(file_name,n)
    #display(sudoku,n,file)
    file = open(file_name+".output","w")


    model = Model('sudoku')

    #VARIABLES
    vars = {}
    for i in range(d):
        for j in range(d):
            for k in range(d):
                vars[i,j,k] = model.addVar(vtype=GRB.BINARY, name='X_'+ str(i)+'_'+str(j)+'_'+str(k))
    model.update()

    #FIXED POSITIONS RESTRICTION
    for i in range(d):
        for j in range(d):
            if sudoku[i][j] != 0:
                v = int(sudoku[i][j]) - 1
                model.addConstr(vars[i,j,v] == 1, 'F_' + str(i) + '_' + str(j))

    #POSITIONS RESTRICTION#
    for i in range(d):
        for j in range(d):
            model.addConstr(quicksum([vars[i,j,v] for v in range(d)]) == 1, 'P_' + str(i) + '_' + str(j))

    #ROWS RESTRICTION
    for i in range(d):
        for k in range(d):
            model.addConstr(quicksum([vars[i,j,v] for j in range(d)]) == 1, 'R_' + str(i) + '_' + str(k))

    #COLUMNS RESTRICTION
    for j in range(d):
        for k in range(d):
            model.addConstr(quicksum([vars[i,j,v] for i in range(d)]) == 1, 'C_' + str(j) + '_' + str(k))

    #BLOCKS RESTRICTION
    for v in range(d):
        for i0 in range(n):
            for j0 in range(n):
                subgrid = [vars[i,j,v] for i in range(i0*n, (i0+1)*n)
                    for j in range(j0*n, (j0+1)*n)]
                model.addConstr(quicksum(subgrid) == 1, 'B_' + str(i0) + '_' + str(j0) + '_' + str(k))


    model.optimize()

    model.write(file_name+".lp")

    solution = model.getAttr('X', vars)

    for i in range(d):
        sol = ''
        for j in range(d):
            for k in range(d):
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
