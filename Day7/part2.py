debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = 40

class Beam:
    def __init__(self, map):
        self._status = (0, [0 for _ in range(len(map[0]))])
        self._stages = []
        self._size = len(map[0])

        for i in range(self._size):
            if map[0][i]=='S':
                self._status[1][i] = 1
        
        for stage in map[1:]:
            s = []
            for i in range(self._size):
                if stage[i] == '^':
                    s.append(i)
            self._stages.append(s)

    def step(self):
        if self.isOver():
            return
        
        stage, beams = self._status
        next_beams = [0 for _ in range(len(beams))]

        for i in range(len(beams)):
            if i not in self._stages[stage]:
                next_beams[i] += beams[i]
            else:
                next_beams[i-1] += beams[i]
                next_beams[i+1] =+ beams[i]
            
            self._status = stage+1, next_beams

    def isOver(self):
        return self._status[0] >= len(self._stages)
    
    def getOutput(self):
        if not self.isOver():
            raise Exception("Beam simulation is not over yet")

        return sum(self._status[1])
        

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