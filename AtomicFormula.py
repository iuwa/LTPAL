import json
import itertools


class AtomicFormula:
    name = ""
    fathers = []
    id = 0
    #newid = itertools.count().__next__
    def __init__(self, name):
        self.name = name
        #self.id = AtomicFormula.newid()
        self.fathers = []

    def get_json(self):
        j =  "{\"name\": \""+str(self.name)+"\", \"fathers\": "+str(self.fathers)+"}"
        
        return json.loads(json.loads(json.dumps(str(j))))


    def __repr__(self):
        j =  "{\"name\": \""+str(self.name)+"\", \"fathers\": "+str(self.fathers)+"}"
        return json.dumps(json.loads(json.loads(json.dumps(str(j)))))

    def setFather(self, father):
        if father not in self.fathers:
            self.fathers.append(father)