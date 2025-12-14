debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = 6

def readInput(f):
    output = []
    for line in f:
        line=line.strip()
        
        op = 0 if line[0]=='L' else 1
        amount = int(line[1:])

        output.append((op, amount))
    
    return output

def solve(model):
    curr = 50
    res = 0

    for op, amount in model:
        
        tmp = curr
        curr = curr+amount if op else curr-amount

        while curr<-100:
            curr += 100
            res +=1

        while curr>100:
            curr-=100
            res +=1

        if (curr<0 and tmp>0) or (curr>100 and tmp!=0):
            res+=1

        curr = curr%100

        if curr==0:
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