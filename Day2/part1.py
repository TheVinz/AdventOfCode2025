debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = 1227775554

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
            s = str(i)
            digits = len(s)
            if digits%2==0:
                l = s[:digits//2]
                r = s[digits//2:]

                if l==r:
                    res += i
                
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