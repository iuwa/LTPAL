# Amirhoshang Hoseinpour Dehkordi

import timeit
import json
from AtomicFormula import AtomicFormula
from OutputClass import OutputClass
from Point import Point
from KripkeModel import KripkeModel
from TransisionSystem import TransisionSystem
import copy
#from MyGame import *

output_log_file = open("output_log_file.log", 'w')


def print_log(s):
    output_log_file.write(str(s)+"\n")
    print(str(s))

print_log("MASKS started ---------------------------------->")

# overlapTresh = 0.5



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
            if ols <= overlapTresh:
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
def subset_knowledge_extraction(atomicFormulaDict, subsetDict):
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



start = timeit.default_timer()
if __name__=="__main__":
    ### initials ....
    allClasses = []
    outputDict = {}
    atomicFormulaDict = {}
    with open('subsetDict.json') as f:
        subsetDict = json.load(f)
    with open('classifiersPredictions.json') as f:
        classifiersPredictions = json.load(f)
    allClasses = classifiersPredictions["allClasses"]
    formulas_PAL = classifiersPredictions["formulas_PAL"]
    formulas_LTPAL = classifiersPredictions["formulas_LTPAL"]
    overlapTresh = classifiersPredictions["overlapTresh"]

    ### Create Atomic formulas
    for i in allClasses:
        atomicFormulaDict[i] = AtomicFormula(i)

    ### PAL side
    #this line should be modified ???? too much fathers willbe added
    print_log("__________Refine Krikpke Model using formulas_PAL_______________")
    atomicFormulaDict = subset_knowledge_extraction(atomicFormulaDict, subsetDict)
    arrayOfkripke = [KripkeModel([0],[(0,0)],{0:[]})]
    for frame_id in range(classifiersPredictions["number_of_frames"]):
        print_log("__________Creating Krikpke Model for frame: "+str(frame_id)+"_______________")
        classifiers_prediction = []
        for tempClassifier in classifiersPredictions["classifiers_ids"]:
            classifiers_prediction.append(classifiersPredictions[tempClassifier][frame_id])
        print_log("__________classifiers_prediction_______________")
        print_log(classifiers_prediction)
        
        arrayOfOutputClasses = []
        for classifier_prediction in classifiers_prediction:
            is_verified, arrayOfOutputClass = classifier_knowledge_calculator(classifier_prediction)
            arrayOfOutputClasses.append(arrayOfOutputClass)
        print_log("__________arrayOfOutputClasses_______________")
        print_log(arrayOfOutputClasses)
        is_verified, kS, arrayOfOutputClasses = MAS_knowledge_aggregator(arrayOfOutputClasses, )
        print_log("__________Intersected arrayOfOutputClasses_______________")
        print_log(arrayOfOutputClasses)
        is_verified, kripke = MAS_knowledge_sharing(arrayOfOutputClasses, kS, atomicFormulaDict )
        kripke_temp = copy.deepcopy(kripke)
        for formula in formulas_PAL:
            remove_list, kripke = MAS_formula_extraction(kripke, formula)
            if remove_list:
                print_log("The input formula: "+formula+" removed list of worlds: "+str(remove_list)+" with names "+
                str(kripke_temp.getVName(remove_list))+" in the kripke Model of frame: "+str(frame_id))
            else:
                print_log("no world removed by PAL formula for frame number: "+str(frame_id))
        arrayOfkripke.append(kripke)

        print_log("__________kripke_______________ for frame number: "+str(frame_id))
        print_log(kripke)
    arrayOfkripke.append(KripkeModel([-1],[(-1,-1)],{-1:[]}))

    #print("The Kripke model is: "+str(arrayOfkripke))

    transitionSystem = create_TS(arrayOfkripke)
    print_log("__________Paths_______________")
    pathes = []
    s_0 = (0,0)
    pathes = transitionSystem.get_all_pathes()
    print_log(pathes)
    print_log("__________Validating Formulas_______________")
    for formula in formulas_LTPAL:
        is_v = 0
        exists = False
        forall = True
        for pi in pathes:
            is_v = check_LTL_valididity(transitionSystem, formula, pi)
            if not exists and is_v:
                exists = True
            if forall and not is_v:
                forall = False
            print_log("The input formula: "+formula+" is evaluated: "+str(is_v)+" in the path: "+str(pi))
        if forall:
            print_log("The input formula: "+formula+" is --verified-- for all paths")
        if exists:
            print_log("The input formula: "+formula+" is --possible-- in some paths")
    print_log("The Transition System model with Probabilities is: "+str(transitionSystem))
    outDict = transitionSystem.get_dict()
    outProb = transitionSystem.get_most_probable_path()
    print_log("__________most_probable_path_______________")
    print_log(outProb)
    print_log("__________most_probable_path_labels_______________")
    print_log(transitionSystem.get_path_names(outProb))
    with open('result.json', 'w') as fp:
        json.dump(outDict, fp)
    #run_anim()
stop = timeit.default_timer()

print_log('runtime: '+ str(stop - start) + " seconds")  


print_log("MASKS ended <------------------------------------")

# config file and a file for each frame, each classifier. 
# get and verify formulas!!
# 