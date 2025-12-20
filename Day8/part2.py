import math

debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = 25272

class Model:
    def __init__(self, coords: list[(int, int, int)]):
        self._junctionBoxes = []
        self._distances = []

        for i in range(len(coords)):
            self._junctionBoxes.append(JunctionBox(i, *coords[i]))
        
        for i in range(len(coords)-1):
            for j in range(i+1, len(coords)):
                self._distances.append(((i,j), distance(coords[i], coords[j])))
        
        self._distances = sorted(self._distances, key=lambda x: x[1])
    
    def solve(self):
        queue = self._distances[:]
        clusters = {jb.cluster:{jb.cluster} for jb in self._junctionBoxes}

        while len(clusters)>1:
            res = 0
            (i,j), _ = queue.pop(0)
            a = self._junctionBoxes[i]
            b = self._junctionBoxes[j]

            if not areConnected(a, b):

                todel = b.cluster
                toupdate = list(clusters[b.cluster])

                clusters[a.cluster] = clusters[a.cluster].union(clusters[b.cluster])

                for x in toupdate:
                    self._junctionBoxes[x].setCluster(a.cluster)

                del clusters[todel]

                res = a.x*b.x

        return res
        

class JunctionBox:
    def __init__(self, id, a, b, c):
        self._coordinates = (a,b,c) 
        self._id = id
        self._cluster = id
    
    def __eq__(self, other):
        if not isinstance(other, JunctionBox):
            return NotImplemented
        return self._id == other.id
    
    def __hash__(self):
        return hash(self._id)
    
    def setCluster(self, id):
        self._cluster = id
    
    @property
    def id(self):
        return self._id
    
    @property
    def cluster(self):
        return self._cluster
    
    @property
    def x(self):
        return self._coordinates[0]

def distance(a, b):
    x1, y1, z1 = a
    x2, y2, z2 = b
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

def areConnected(a: JunctionBox, b: JunctionBox) -> bool:
    return a.cluster == b.cluster

def readInput(f):
    res = []

    for line in f:
        line = line.strip()

        coords = [int(x) for x in line.split(',')]
        res.append(coords)
    
    return Model(res)

def solve(model: Model) -> int:
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