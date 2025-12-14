debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = 3121910778619

def getmaxidx(bunk, start, end):
    m = bunk[start]
    idx = start

    for i in range(start, len(bunk)-end):
        if bunk[i]>m:
            m = bunk[i]
            idx=i
    
    return m, idx

def readInput(f):
    output = []
    for line in f:
        output.append([int(i) for i in line.strip()])
    
    return output

def solve(model):
    res = 0

    for bunk in model:
        joltage = []
        x=-999
        idx=-1
        for i in range(12, 0, -1):
            x, idx = getmaxidx(bunk, idx+1, i-1)
            joltage.append(x)
        
        res += int(''.join([str(i) for i in joltage]))

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