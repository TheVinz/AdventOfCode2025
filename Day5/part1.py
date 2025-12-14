debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = 3

class Database:
    def __init__(self):
        self._ranges = []
        self._ids = []
    
    @property
    def ranges(self):
        return self.ranges[:]
    
    @property
    def ids(self):
        return self._ids[:]

    def putID(self, id):
        self._ids.append(id)
    
    def putRange(self, a, b=None):
        if b is None and isinstance(a, tuple):
            r = a
        else:
            r = (a,b)

        self._ranges.append(r)

    def getRange(self, idx):
        return self._ranges[idx]

    def getID(self, idx):
        return self._ids[idx]
    
    def isFresh(self, id):
        for a,b in self._ranges:
            if id>=a and id<=b:
                return True
        
        return False


def readInput(f):
    model = Database()
    check = False

    for line in f:
        line = line.strip()
        if line == '':
            check = True
        elif check:
            model.putID(int(line))
        else:
            a,b = line.split('-')
            model.putRange(int(a), int(b))
    
    return model



def solve(model: Database) -> int:
    res = 0

    for id in model.ids:
        if model.isFresh(id):
            res += 1
    
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