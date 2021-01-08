import spacy 
import math
import networkx as nx
from networkx.algorithms import *


nlp = spacy.load('en_core_web_sm') 
  



def get_prob(set0, set1):
    G = nx.Graph()
    temp_set0 = []
    temp_set1 = []
    for i in range(len(set0)+len(set1)):
        if i < len(set0):
            temp_set0.append(set0[i]+"_0")
            G.add_node(set0[i]+"_0")
        else:
            G.add_node(str(i)+"_0")
            temp_set0.append(str(i)+"_0")
        if i < len(set1):
            temp_set1.append(set1[i]+"_1")
            G.add_node(set1[i]+"_1")
        else:
            G.add_node(str(i)+"_1")
            temp_set1.append(str(i)+"_1")
    for i in temp_set0:
        for j in temp_set1:
            words = i[:-2]+" "+j[:-2]  
            tokens = nlp(words) 
            token1, token2 = tokens[0], tokens[1]
            G.add_edge(i, j, weight=abs(math.log(token1.similarity(token2))) )
    
    matchingTemp = list(max_weight_matching(G, maxcardinality=False, weight='weight'))
    prob = 0.0
    for i in matchingTemp:
        words = i[0][:-2]+" "+i[1][:-2]
        tokens = nlp(words) 
        token1, token2 = tokens[0], tokens[1]
        prob += math.log(token1.similarity(token2))
    return math.exp(prob)


if __name__=="__main__":
    set0 = ["cat", "dog"]
    set1 = ["cat", "chair"]
    matchingTemp  = get_prob(set0, set1)