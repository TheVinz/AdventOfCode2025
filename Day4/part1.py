debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = 13

A = 0
B = 0

def getAdjNumber(i, j, matrix):
    res=0
    adjIdxs = getAdjIdxs(i,j)

    for x,y in adjIdxs:
        res += matrix[x][y]
        
    return res

def getAdjIdxs(i, j):
    res = []
    for x in range(i-1, i+2):
        for y in range(j-1,j+2):
            if x>=0 and y>=0 and x<A and y<B and (x!=i or y!=j):
                res.append((x,y))
    
    return res

def readInput(f):
    global A
    global B

    output = []

    for line in f:
        line = line.strip()

        output.append(list(map(lambda x: 0 if x=='.' else 1, line)))
    
    A = len(output)
    B = len(output[0])

    return output

def solve(model):
    res = 0

    for i in range(A):
        for j in range(B):
            if model[i][j] and getAdjNumber(i, j, model)<4:
                res+=1
    
    return res

if __name__=='__main__':
    with open(debug_filename, 'r') as f:
        model = readInput(f)
    res = solve(model)

    if res == DEBUG:
        print("Debug test passed, running on probelm input...")
    else:
        print("Debug test failed.\nExpected output: {}\nActual output: {}".format(DEBUG, res))
        exit(-1)
    
    with open(input_filename, 'r') as f:
        model = readInput(f)
    print(solve(model))