debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = 4174379265

def isvalid(id):
    s = str(id)
    digits = len(s)

    for i in range(2, digits+1):
        if digits%i==0:
            l = digits//i
            p = s[:l]
            ps = p*i

            if ps==s:
                return False

    return True


def readInput(f):
    output = []

    line = f.readlines()[0].strip()
    for i in line.split(','):
        a,b = i.split('-')
        
        output.append((int(a), int(b)))

    return output

def solve(model):
    res = 0

    for a,b in model:
        for i in range(a, b+1):
            if not isvalid(i):
                res+=i
    
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