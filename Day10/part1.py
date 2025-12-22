import re

debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = 7

def press(lights, button):
    lights = list(lights)
    for b in button:
        lights[b] = not lights[b]
    
    return tuple(lights)

class Entry:
    def __init__(self, lights, buttons, joltages):
        self.lights = lights
        self.buttons = buttons
        self.joltages = joltages
    
    def solve(self):
        it = 1
        state = set([(tuple([False]*len(self.lights)),button) for button in self.buttons])
        visited = set(state)

        while True:
            new_state = set()
            for lights, button in state:
                lights = press(lights, button)
                if lights == self.lights:
                    return it
                for b in self.buttons:
                    if b!=button and (lights, b) not in visited:
                        new_state.add((lights, b))
            state = new_state
            visited.update(state)
            if not state:
                raise Exception('Empty state')
            it += 1
        

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
    return sum([x.solve() for x in model])

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