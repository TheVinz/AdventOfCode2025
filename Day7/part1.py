debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = 21

class Beam:
    def __init__(self, map):
        self._status = (0, {})
        self._stages = []
        self._size = len(map[0])
        self._split = 0

        for i in range(self._size):
            if map[0][i]=='S':
                self._status = (0, {i})
        
        for stage in map[1:]:
            s = []
            for i in range(self._size):
                if stage[i] == '^':
                    s.append(i)
            self._stages.append(s)

    def step(self):
        if self.isOver():
            return
        
        stage, beam = self._status
        next_beam = set()

        for b in beam:
            if b not in self._stages[stage]:
                next_beam.add(b)
            else:
                next_beam.add(b-1)
                next_beam.add(b+1)
                self._split += 1
        
        self._status = stage+1, next_beam

    def isOver(self):
        return self._status[0] >= len(self._stages)
    
    def getOutput(self):
        if not self.isOver():
            raise Exception("Beam simulation is not over yet")

        return self._split
        

def readInput(f):
    lines = []

    for line in f:
        lines.append(line.strip())
    
    return Beam(lines)

def solve(model: Beam) -> int:
    while not model.isOver():
        model.step()
    
    return model.getOutput()
    

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