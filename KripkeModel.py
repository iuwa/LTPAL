class KripkeModel:
    W = []
    R = []
    V = {}
    def __init__(self, W, R, V):
        self.W = W
        self.R = R
        self.V = V

    def setWRVFull(self, worldID, v):
        self.W.append(worldID)
        self.V[worldID]=v
        for i in self.W:
            if i != worldID:
                self.R.append((i,worldID))
            self.R.append((worldID,i))
   

    def removeWorld(self, w):
        self.W.remove(w)
        removeList = []
        for i in self.R:
            if i[0] == w or i[1]==w:
                removeList.append(i)
        for i in removeList:
            self.R.remove(i)
        self.V.pop(w)

    def getVName(self, temp_list):
        res_list = []
        for i in temp_list:
            temp_names = []
            for j in self.V[i]:
                temp_names.append(j.get_json()["name"])
            res_list.append(temp_names)
        return res_list

    def __repr__(self):
        return "(\nW="+str(self.W)+",\nR="+str(self.R)+",\nV="+str(self.V)+")" 