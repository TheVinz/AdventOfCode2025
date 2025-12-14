debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = 3263827

def toNumber(digits):
    res = []

    for digit in digits:
        if digit != ' ':
            res.append(digit)
    
    if res==[]:
        return None
    else:
        return int(''.join(res))
    

class Worksheet:
    def __init__(self, ops, *args):
        self._problems = []
        terms = []

        for i in range(len(args[0])):
            digits = [arg[i] for arg in args]
            val = toNumber(digits)

            if val is None:
                temp = ops.pop(0), terms
                self._problems.append(temp)
                terms = []
            else:
                terms.append(val)
        
        temp = ops.pop(), terms
        self._problems.append(temp)
        


    
    @property
    def problems(self):
        return self._problems[:]
    
    def solve(self, idx=None):
        if idx==None:
            res=0
            
            for i in range(len(self._problems)):
                res += self.solve(i)
            
            return res
        
        else:
            op, args = self._problems[idx]

            if op=='*':
                res = 1
                for arg in args:
                    res = res*arg
                return res
            elif op=='+':
                res = 0
                for arg in args:
                    res += arg
                return res
            else:
                raise Exception(f'Invalid op: {op}')
        
def readInput(f):
    lines = []
    
    for line in f:
        lines.append(line.replace('\n', ''))

    res = Worksheet(lines[-1].strip().split(), *lines[:-1])

    return res

def solve(model):
    return model.solve()

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