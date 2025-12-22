import re
import time

debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = 33
EPSILON = 1e-8

def getFloadIdx(x):
    for i in range(len(x)):
        if abs(x[i]-round(x[i])) > 1e-08:
            return i
    
    raise Exception(f"Invalid integer vector {x}")

def hasFloat(x):
    return any([abs(i-round(i)) > 1e-8 for i in x])

def branch_and_bound(inA, inb):

    queue = [(inA, inb, [1]*len(inA[0]), ["eq"]*len(inb))]
    out = None, None
    best = float("inf")

    while queue:

        A, b, c, ops = queue.pop(0)
        x, res = two_phase_simplex(A, b, c=c, ops=ops)


        if res is not None:
            res = -res
            if res < best:
                if not hasFloat(x):
                    best = res
                    out = x, res
                else:
                    idx = getFloadIdx(x)

                    newrow = [0]*len(A[0])
                    newrow[idx] = 1

                    queue.append((A+[newrow], b + [int(x[idx])], c, ops + ['leq']))
                    queue.append((A+[newrow], b + [int(x[idx])+1], c, ops + ['geq']))

    return out


def transpose(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]


def two_phase_simplex(A, b, c=None, ops=None):
    if ops is None:
        ops = ['eq']*len(b)
    
    if c is None:
        c = [1]*len(A[0])

    A = [row[:] for row in A]
    b = b[:]
    c = c[:]
    
    for i in range(len(b)):
        if b[i] < 0:
            b[i] = -b[i]
            A[i] = [-A[i][j] for j in range(len(A[i]))]
            if ops[i] == 'leq':
                ops[i] = 'geq'
            elif ops[i] == 'geq':
                ops[i] = 'leq'
    
    s = sum([1 for x in ops if x in ['leq', 'geq']])
    a = sum([1 for x in ops if x in ['eq', 'geq']])
    n = len(c)
    m = len(A)
    
    tableau = []
    basis = []
    i_s = 0  
    i_a = 0  

    for i in range(m):
        row = A[i] + [0]*(s+a) + [b[i]]
        
        if ops[i] == 'leq':
            row[n + i_s] = 1
            basis.append(n + i_s)
            i_s += 1
        elif ops[i] == 'geq':
            row[n + i_s] = -1
            row[n + s + i_a] = 1
            basis.append(n + s + i_a)
            i_s += 1
            i_a += 1
        else: 
            row[n + s + i_a] = 1
            basis.append(n + s + i_a)
            i_a += 1

        tableau.append(row)
    
    obj_row = [0]*(n+s) + [1]*a + [0]

    for i in range(m):
        if basis[i] >= n+s:  
            for j in range(n+s+a+1):
                obj_row[j] -= tableau[i][j]
    
    tableau.append(obj_row)

    tableau, basis = run_simplex(tableau, basis, n + s + a, m)

    if tableau is None:
        return None, None
    
    if abs(tableau[-1][-1]) > 1e-8:
        return None, None
    
    artificial_in_basis = [i for i in range(m) if basis[i] >= n+s]
    
    if artificial_in_basis:
        for row_idx in artificial_in_basis:
            pivoted = False
            for col_idx in range(n + s):
                if abs(tableau[row_idx][col_idx]) > 1e-10:
                    if col_idx not in basis:
                        pivot_element = tableau[row_idx][col_idx]
                        
                        for j in range(n + s + a + 1):
                            tableau[row_idx][j] /= pivot_element
                        
                        for i in range(m + 1):
                            if i != row_idx:
                                multiplier = tableau[i][col_idx]
                                for j in range(n + s + a + 1):
                                    tableau[i][j] -= multiplier * tableau[row_idx][j]
                        
                        basis[row_idx] = col_idx
                        pivoted = True
                        break
            
            if not pivoted:
                pass
    
    tableau2 = []
    for i in range(m):
        tableau2.append(tableau[i][:n+s] + [tableau[i][-1]])
    
    obj_row = c + [0]*(s + 1)

    for i in range(m):
        if basis[i] < n+s:  
            coef = obj_row[basis[i]]
            if abs(coef) > 1e-10:
                for j in range(n + s + 1):
                    obj_row[j] -= coef * tableau2[i][j]
    
    tableau2.append(obj_row)
    
    tableau2, basis = run_simplex(tableau2, basis, n + s, m)

    if tableau2 is None:
        return None, None
    
    x = [0.0] * n
    for i in range(m):
        if basis[i] < n:
            x[basis[i]] = tableau2[i][-1]
    
    obj_value = tableau2[-1][-1]
    
    return x, obj_value


def run_simplex(tableau, basis, num_vars, m):
    iteration = 0
    max_iterations = 1000
    
    while iteration < max_iterations:
        obj_row = tableau[-1]
        
        entering = -1
        min_val = -1e-10
        
        for j in range(num_vars):
            if obj_row[j] < min_val:
                min_val = obj_row[j]
                entering = j
        
        if entering == -1:
            return tableau, basis
        
        iteration += 1
        
        leaving = -1
        min_ratio = float('inf')
        
        for i in range(m):
            if tableau[i][entering] > 1e-10:
                ratio = tableau[i][-1] / tableau[i][entering]
                if ratio >= -1e-10 and ratio < min_ratio: 
                    min_ratio = ratio
                    leaving = i
        
        if leaving == -1:
            return None, None
                
        pivot = tableau[leaving][entering]
        
        for j in range(num_vars + 1):
            tableau[leaving][j] /= pivot
        
        for i in range(m + 1):
            if i != leaving:
                multiplier = tableau[i][entering]
                for j in range(num_vars + 1):
                    tableau[i][j] -= multiplier * tableau[leaving][j]
        
        basis[leaving] = entering
    
    return None, None


class Entry:
    def __init__(self, lights, buttons, joltages):
        self.lights = lights
        self.joltages = joltages
        self.buttons = buttons
    
    def solve(self):

        buttons = []
        for b in self.buttons:
            res = [0]*len(self.joltages)
            for bb in b:
                res[bb]=1
            buttons.append(res)
        
        A = transpose(buttons)
        
        _, res = branch_and_bound(A, list(self.joltages))
                
        return res    
        

def readInput(f):
    model = []

    for line in f:
        line = line.strip()
        res = re.match(r"\[([.#]+)\]((?:\s+\(\d+(?:,\d+)*\))*)\s+\{(\d+(?:,\d+)*)\}", line)

        lights = tuple([c=='#' for c in res.group(1).strip()])
        buttons = [tuple([int(x) for x in b.strip().replace('(', '').replace(')', '').split(',')]) for b in res.group(2).strip().split(' ')]
        joltage = tuple(map(lambda x: int(x), res.group(3).replace('{', '').replace('}', '').split(',')))

        model.append(Entry(lights, buttons, joltage))
    
    return model
        

def solve(model):
    res = 0
    for x in model:
        res += x.solve()
    
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