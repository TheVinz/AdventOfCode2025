debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = 357

def readInput(f):
    output = []
    for line in f:
        output.append([int(i) for i in line.strip()])
    
    return output

def solve(model):
    res = 0

    for bunk in model:
        a = bunk[0]
        idx = 0
        for i in range(len(bunk)-1):
            if bunk[i]>a:
                a=bunk[i]
                idx=i
        
        b = max(bunk[idx+1:])

        res += a*10 + b

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