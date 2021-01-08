
from Point import Point

class OutputClass:
    name = ""
    tl = Point(10, 10)
    br = Point(20, 20)

    def __init__(self, name, tl, br):
        self.name = name
        x = br.x - tl.x
        y = br.y - tl.y
        if x<0:
            temp = tl.x
            tl.x = br.x
            br.x = temp
        if y<0:
            temp = tl.y
            tl.y = br.y
            br.y = temp
        self.tl = tl
        self.br = br

    def __repr__(self):
        return "("+str(self.name)+","+str(self.tl)+","+str(self.br)+")" 
