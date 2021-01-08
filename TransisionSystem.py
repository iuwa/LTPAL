from KripkeModel import KripkeModel
from GetProb import *
import json

class TransisionSystem:
    S = []
    R = []
    s_0 = 0
    s_1 = -1
    Arrow = []
    L = {}
    arrowProbability = {}
    len = 0
    def __init__(self, S, R, s_0, s_1, Arrow, L):
        self.S = S
        self.R = R
        self.s_0 = s_0
        self.s_1 = s_1
        self.Arrow = Arrow
        self.L = L
        self.len = 0
        self.arrowProbability = {}

    def add_kripke(self, kripke):
        dualW = [(self.len, i) for i in kripke.W]
        self.S.append(dualW)
        tempR = []
        for i in kripke.R:
            tempR.append(((self.len, i[0]),(self.len, i[1])))
        self.R.append(tempR)
        for i in dualW:
            self.L[i] = kripke.V[i[1]]
        if self.len:
            for i in self.S[self.len-1]:
                for j in kripke.W:
                    self.Arrow.append((i,(self.len, j)))
                    #self.arrowProbability[(i,(self.len, j))] = 1#i[0]+i[1]+1+j
                    self.set_probability((i,(self.len, j)))
        self.len += 1
            
    def get_kripke(self, w):
        W = self.S[w[0]]
        R = self.R[w[0]]
        V = {}
        for i in self.L:
            if i[0] == w[0]:
               V[i]=self.L[i]
        kripke = KripkeModel(W, R, V)
        return kripke
    
    def set_probability(self, arrow):
        set1 = []
        set0 = []
        for i in json.loads(json.loads(json.dumps(str(self.L[arrow[0]])))):
            set0.append(i["name"])
        for i in json.loads(json.loads(json.dumps(str(self.L[arrow[1]])))):
            set1.append(i["name"])
        self.arrowProbability[arrow] = get_prob(set0, set1)
        return 0

    def get_most_probable_path(self):
        path = {(0,0):None}
        prob = {(0,0):1.0}
        lastNode = (0,0)
        for i in range(self.len-1):
            for j in self.S[i]:
                for k in self.S[i+1]:
                    if (j,k) in self.arrowProbability:
                        if k in prob:
                            if prob[j]*self.arrowProbability[(j,k)] > prob[k]:
                                prob[k] = prob[j]*self.arrowProbability[(j,k)]
                                path[k] = j
                                lastNode = k
                        else:
                            prob[k] = prob[j]*self.arrowProbability[(j,k)]
                            path[k] = j
                            lastNode = k

        tempPath = []
        while lastNode:
            tempPath.insert(0,lastNode)
            lastNode = path[lastNode]
        return tempPath

    def get_all_pathes(self):
        pathes = [[(0,0)]]
        for i in range(self.len):
            for j in pathes:
                if len(j) == i+1:
                    for k in range(len(self.Arrow)):
                        if self.Arrow[k][0] == j[-1]:
                            tempArray = j.copy()
                            tempArray.append(self.Arrow[k][1])
                            pathes.append(tempArray)
        tempPathes = []
        for i in pathes:
            if len(i) == self.len:
                tempPathes.append(i)
        return tempPathes

    def get_dict(self):
        outDict = {}
        outDict["S"] = self.S
        outDict["R"] = self.R
        outDict["s_0"] = self.s_0
        outDict["s_1"] = self.s_1
        outDict["Arrow"] = self.Arrow
        lDict = {}
        for i in self.L:
            tempArr = []
            for j in self.L[i]:
                tempArr.append(json.loads(json.loads(json.dumps(str(j)))))
            lDict[str(i[0])+"_"+str(i[1])] =tempArr
            
        outDict["L"] = lDict
        return outDict

    def __repr__(self):
        return "(\nS="+str(self.S)+",\nR="+str(self.R)+",\ns_0="+str(self.s_0)+",\ns_1="+str(self.s_1)+",\nArrow="+str(self.Arrow)+",\nL="+str(self.L)+",\narrowProbability="+str(self.arrowProbability)+")" 