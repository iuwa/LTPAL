import timeit

start = timeit.default_timer()
import json
from AtomicFormula import AtomicFormula
from OutputClass import OutputClass
from Point import Point
from KripkeModel import KripkeModel
from TransisionSystem import TransisionSystem
#from MyGame import *

print("MASKS started ---------------------------------->")

overlapTresh = 0.5



class Formulas:
    pass


def powerset(s):
    x = len(s)
    powerSet = []
    for i in range(1 << x):
        powerSet.append([s[j] for j in range(x) if (i & (1 << j))])
    return powerSet


def calcOverlap(a, b):  
    dx = min(a.br.x, b.br.x) - max(a.tl.x, b.tl.x)
    dy = min(a.br.y, b.br.y) - max(a.tl.y, b.tl.y)
    x = a.br.x - a.tl.x
    y = a.br.y - a.tl.y
    if (dx>=0) and (dy>=0):
        area = (dx*dy)/(x*y)
        if area > 1:
            area = 1
        return area
    return 0.0


def overlapOfList(kSPs, arrayOfOutputClasses):
    maxOverlap = 0.0
    for i in arrayOfOutputClasses:
        for j in i:
            for k in i:
                names = [nn.name for nn in kSPs]
                if j.name in names and k.name in names and k!=j:
                    calcO = calcOverlap(j, k)
                    if calcO > maxOverlap:
                        maxOverlap = calcO
    return maxOverlap


def classifier_knowledge_calculator(classifier):
    arrayOfOutputClasses = []
    for output in classifier:
        arrayOfOutputClasses.append(OutputClass(output['name'], Point(output['tl']["x"], output['tl']["y"]), Point(output['br']["x"], output['br']["y"])))
    if len(arrayOfOutputClasses) == 1:
        return 1, arrayOfOutputClasses
    return 0, arrayOfOutputClasses


# collecting classifiers' knowledge
def MAS_knowledge_aggregator(arrayOfOutputClasses, ):
    if not arrayOfOutputClasses:
        return 0, [], []
    kS = allClasses
    tempArrayOfOutputClasses = []
    for outputClasses in arrayOfOutputClasses:
        k = []
        tempArrayOfOutputClass = []
        for outputClass in outputClasses:
            k.append(outputClass.name)
        kS = list(set(kS) & set(k))
        if not kS:
            return 0, kS, []
    tempArrayOfOutputClasses = []
    for outputClasses in arrayOfOutputClasses:
        tempArrayOfOutputClass = []
        for outputClass in outputClasses:
            if outputClass.name in kS:
                tempArrayOfOutputClass.append(outputClass)
        tempArrayOfOutputClasses.append(tempArrayOfOutputClass)
    if len(kS) == 1:
        return 1, kS, tempArrayOfOutputClasses
    return 0, kS, tempArrayOfOutputClasses


def MAS_knowledge_sharing(arrayOfOutputClasses, kS, atomicFormulaDict ):
    if not arrayOfOutputClasses:
        return 0, arrayOfOutputClasses
    atomicFormulaArray = []
    for i in kS:
        atomicFormulaArray.append(atomicFormulaDict[i])

    kSPowerSet = powerset(atomicFormulaArray)
    kSPowerSetOL = []
    for kSPs in kSPowerSet:
        if len(kSPs) > 1:
            ols = overlapOfList(kSPs, arrayOfOutputClasses)
            if ols < overlapTresh:
                kSPowerSetOL.append(kSPs)
        elif len(kSPs) == 1:
            kSPowerSetOL.append(kSPs)
    worldID = 0
    kripke = KripkeModel([],[],{})
    for i in kSPowerSetOL:
        worldID += 1
        v = i
        kripke.setWRVFull(worldID, v)
    

    return 0, kripke


# create parental relation for atomic formulas
def single_framed_knowledge_extraction(atomicFormulaDict, subsetDict):
    for i in subsetDict:
        if i not in atomicFormulaDict:
            atomicFormulaDict[i]=AtomicFormula(i)
        for j in subsetDict[i]:
            if j not in atomicFormulaDict:
                atomicFormulaDict[j]=AtomicFormula(j)
            atomicFormulaDict[i].setFather(atomicFormulaDict[j])
    return atomicFormulaDict

def token_formula(formula):
    formula1 = ""
    formula2 = ""
    parenthesesCounter = 0
    state = 0
    for i in formula[1:-1]:
        if i == "(":
            parenthesesCounter += 1
        elif i== ")":
            parenthesesCounter -= 1
        if parenthesesCounter < 0:
            return "", ""
        if parenthesesCounter == 0 and i == ",":
            state += 1
            if state > 1:
                return "", ""
            continue
        if state:
            formula2 += i
        else:
            formula1 += i
    return formula1, formula2


def is_PAL_formula(formula):
    if not formula:
        return 0
    elif formula[0] == "~":# not \varphi = ~\varphi
        return is_PAL_formula(formula[1:])
    elif formula[0] == "&":# \varphi \land \psi= &(\varphi,\psi)
        formula1, formula2 = token_formula(formula[1:])
        return is_PAL_formula(formula1) and is_PAL_formula(formula2) 
    elif formula[0] == "|":# \varphi \lor \psi= |(\varphi,\psi)
        formula1, formula2 = token_formula(formula[1:])
        return is_PAL_formula(formula1) and is_PAL_formula(formula2) 
    elif formula[0:3] == "K_i":# K_i\varphi 
        return is_PAL_formula(formula[3:]) 
    else:
        if formula in allClasses:
            return 1
    return 0


def check_PAL_valididity(kripke, formula, w):
    if not formula:
        return 0
    elif formula[0] == "~":# not \varphi = ~\varphi
        return not check_PAL_valididity(kripke, formula[1:], w)
    elif formula[0] == "&":# \varphi \land \psi= &(\varphi,\psi)
        formula1, formula2 = token_formula(formula[1:])
        return check_PAL_valididity(kripke, formula1, w) and check_PAL_valididity(kripke, formula2, w) 
    elif formula[0] == "|":# \varphi \lor \psi= |(\varphi,\psi)
        formula1, formula2 = token_formula(formula[1:])
        return check_PAL_valididity(kripke, formula1, w) or check_PAL_valididity(kripke, formula2, w) 
    elif formula[0:3] == "K_i":# K_i\varphi 
        for i in kripke.R:
            if i[0] == w:
                if not check_PAL_valididity(kripke, formula[3:], i[1]):
                    return 0
        return 1 
    else:
        for i in kripke.V[w]:
            if formula == i.name:
                return 1
    return 0


def MAS_formula_extraction(kripke, formula):
    removeList = []
    for w in kripke.W:
        if not check_PAL_valididity(kripke, formula, w):
            removeList.append(w)
    for i in removeList:
        kripke.removeWorld(i)
    return removeList, kripke


def create_TS(arrayOfkripke):
    transitionSystem = TransisionSystem([],[],0,-1,[],{})
    for kripke in arrayOfkripke:
        transitionSystem.add_kripke(kripke)

    return transitionSystem



def check_LTL_valididity(transitionSystem, formula, pi):
    if len(pi) == 1:
        return 1
    if not formula:
        return 0
    elif is_PAL_formula(formula):
        return check_PAL_valididity(transitionSystem.get_kripke(pi[0]), formula, pi[0])
    elif formula[0] == "~":
        return not check_LTL_valididity(transitionSystem, formula[1:], pi)
    elif formula[0] == "&":
        formula1, formula2 = token_formula(formula[1:])
        return check_LTL_valididity(transitionSystem, formula1, pi) and check_LTL_valididity(transitionSystem, formula2, pi) 
    elif formula[0] == "|":
        formula1, formula2 = token_formula(formula[1:])
        return check_LTL_valididity(transitionSystem, formula1, pi) or check_LTL_valididity(transitionSystem, formula2, pi) 
    elif formula[0:3] == "X_i":
        return check_LTL_valididity(transitionSystem, formula[3:], pi[1:])
    elif formula[0:3] == "U_i":
        formula1, formula2 = token_formula(formula[3:])
        if check_LTL_valididity(transitionSystem, formula2, pi):
            return 1
        while not check_LTL_valididity(transitionSystem, formula2, pi):
            if not check_LTL_valididity(transitionSystem, formula1, pi):
                return 0
            pi = pi[1:]
        return 1
    else:
        pass
        #?????????????????????? LTL operators
    return 0

allClasses = []
if __name__=="__main__":
    ### initials ....
    outputDict = {}
    atomicFormulaDict = {}
    with open('subsetDict.json') as f:
        subsetDict = json.load(f)
    with open('classifiersPredictions.json') as f:
        classifiersPredictions = json.load(f)
    allClasses = classifiersPredictions["allClasses"]
    formulas_PAL = classifiersPredictions["formulas_PAL"]
    formulas_LTPAL = classifiersPredictions["formulas_LTPAL"]

    ### Create Atomic formulas
    for i in allClasses:
        atomicFormulaDict[i] = AtomicFormula(i)

    ### PAL side
    #this line should be modified ????
    atomicFormulaDict = single_framed_knowledge_extraction(atomicFormulaDict, subsetDict)
    arrayOfkripke = [KripkeModel([0],[(0,0)],{0:[]})]
    for frame in range(classifiersPredictions["len"]):
        classifiers = []
        for tempClassifier in classifiersPredictions["ids"]:
            classifiers.append(classifiersPredictions[tempClassifier][frame])
        arrayOfOutputClasses = []
        for classifier in classifiers:
            is_verified, arrayOfOutputClass = classifier_knowledge_calculator(classifier)
            arrayOfOutputClasses.append(arrayOfOutputClass)
        is_verified, kS, arrayOfOutputClasses = MAS_knowledge_aggregator(arrayOfOutputClasses, )
        is_verified, kripke = MAS_knowledge_sharing(arrayOfOutputClasses, kS, atomicFormulaDict )
        for formula in formulas_PAL:
            remove_list, kripke = MAS_formula_extraction(kripke, formula)
            print("The input formula: "+formula+" is removed list: "+str(remove_list)+" of worlds in the kripke: "+str(kripke))
        arrayOfkripke.append(kripke)

    arrayOfkripke.append(KripkeModel([-1],[(-1,-1)],{-1:[]}))

    #print("The Kripke model is: "+str(arrayOfkripke))

    transitionSystem = create_TS(arrayOfkripke)

    for formula in formulas_LTPAL:
        s_0 = (0,0)
        pathes = transitionSystem.get_all_pathes()
        print("__________PATHES_______________")
        print(pathes)
        is_v = 0
        for pi in pathes:
            is_v = check_LTL_valididity(transitionSystem, formula, pi)
            print("The input formula is evaluated: "+str(is_v)+" in the path: "+str(pi))
    print("The Transition System model is: "+str(transitionSystem))
    outDict = transitionSystem.get_dict()
    outProb = transitionSystem.get_most_probable_path()
    print("+++++++++++++++++++++++++++++")
    print(outProb)
    with open('result.json', 'w') as fp:
        json.dump(outDict, fp)
    #run_anim()

print("MASKS ended <------------------------------------")
stop = timeit.default_timer()

print('Time: ', stop - start)  