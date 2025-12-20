debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = 50

def mod(x):
    if x<0:
        return -x
    return x

def readInput(f):
    res = []

    for line in f:
        line = line.strip()
        a,b = line.split(',')
        res.append((int(a), int(b)))
    
    return res


def solve(model):
    res = 0

    for i in range(len(model)-1):
        for j in range(i+1, len(model)):
            x1, y1 = model[i]
            x2, y2 = model[j]

            area = (mod(x1-x2)+1)*(mod(y1-y2)+1)

            if area>res:
                res=area
    
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