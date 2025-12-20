debug_filename = 'debug.txt'
input_filename = 'input.txt'

DEBUG = 24

def doesIntersect(p1,p2,p3,p4):
    x1,y1 = p1
    x2,y2 = p2
    x3,y3 = p3
    x4,y4 = p4

    if x1==x2 and y3==y4:
        x=x1
        y=y3
        return min(x3,x4)<x<max(x3,x4) and min(y1,y2)<y<max(y1,y2)
    if y1==y2 and x3==x4:
        x=x3
        y=y4
        return min(x1,x2)<x<max(x1,x2) and min(y3,y4)<y<max(y3,y4)

    return False

class Map:
    def __init__(self, model, sizex, sizey):
        self._points = model
        self._maxx = sizex
        self._maxy = sizey
    
    def isInside(self, point):

        x, y = point
        inside = False
        n = len(self._points)

        for i in range(n):
            a = self._points[i]
            b = self._points[(i+1)%n]

            xa,ya = a
            xb,yb = b

            if xa==xb and x==xa and min(ya,yb)<=y<=max(ya,yb):
                return True
            if ya==yb and y==ya and min(xa,xb)<=x<=max(xa,xb):
                return True

            if xa==xb and xa>x and min(ya,yb)<y<=max(ya,yb):
                inside = not inside
        
        return inside

    def isValid(self, a, b):
        x1, y1 = a
        x2, y2 = b

        n = len(self._points)

        if not self.isInside((x1,y2)):
            return False
        if not self.isInside((x2, y1)):
            return False
        
        for i in range(n):
            p1 = self._points[i]
            p2 = self._points[(i+1)%n]

            if doesIntersect((x1,y1), (x1,y2), p1, p2) or \
                doesIntersect((x1,y2), (x2,y2), p1, p2) or \
                doesIntersect((x2,y2), (x2,y1), p1, p2) or \
                doesIntersect((x2,y1), (x1,y1), p1, p2):
                return False

        return True

    
    def solve(self):
        res = 0

        for i in range(len(self._points)-1):
            print(f'{i}/{len(self._points)}', end='\r')
            for j in range(i+1, len(self._points)):
                a = self._points[i]
                b = self._points[j]

                if self.isValid(a,b):
                    x1, y1 = a
                    x2, y2 = b
                    area = (mod(x1-x2)+1)*(mod(y1-y2)+1)

                    if area > res:
                        res = area

                
        return res


def mod(x):
    if x<0:
        return -x
    return x

def readInput(f):
    res = []

    for line in f:
        line = line.strip()
        a,b = line.split(',')
        res.append((int(a), int(b)))
    
    sizex = max([x for x,_ in res]) + 1
    sizey = max([y for _,y in res]) + 1

    return Map(res, sizex, sizey)

def solve(model):
    res = model.solve()

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