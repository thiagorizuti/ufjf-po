from sys import argv

def read_sudoku_file(file_name):
    with open(file_name,"r") as file:
        content = file.readlines()
        sudoku = []
        for line in content:
            row = [int(n) for n in line.split()]
            sudoku.append(row)
    return sudoku

def calculate_fitness(sudoku,dim):
    return columns_fitness(sudoku,dim) + blocks_fitness(sudoku,dim) + rows_fitness(sudoku,dim);

def rows_fitness(sudoku,dim):
    fit = 0
    for row in sudoku:
        v = [0 for x in range(dim**2)]
        for i in range(len(row)):
            v[row[i]-1] += 1
        for x in v:
            fit += abs(x-1)
    return fit

def blocks_fitness(sudoku,dim):
    fit = 0
    v = [0 for x in range(dim**2)]
    for m in range(dim):
        for n in range(dim):
            for i in range(m*dim, m*dim	 + dim):
                for j in range(n*dim, n*dim + dim):
                    v[sudoku[i][j]-1] += 1
            for x in v:
                fit += abs(x-1)
            v = [0 for x in range(dim**2)]
    return fit

def columns_fitness(sudoku,dim):
    fit = 0
    for i in range(dim**2):
        v = [0 for x in range(dim**2)]
        for row in sudoku:
            v[row[i]-1] += 1
        for x in v:
            fit += abs(x-1)
    return fit

def main():
    if len(argv) < 3:
        print "First argument: file name.argument"
        print "Second argument: sudoku dimension"
        return 1
    dim = int(argv[1])
    file_name = argv[2]
    sudoku = read_sudoku_file(file_name)
    print calculate_fitness(sudoku,dim)
    return 0
if __name__ == "__main__":
    main()
