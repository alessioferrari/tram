'''
Created on Jan 20, 2014

@author: alessioferrari
'''
from RequirementsModel import RequirementsModel

class ObjectChangeTransformation(object):
    '''
    This class is a transformation that transform 
    a RequirementsModel into another by changing
    the object
    '''


    def __init__(self, oldObjectString, newObjectString):
        '''
        Constructor
        '''
        self.oldObjectString = oldObjectString
        self.newObjectString = newObjectString
        
    def transform(self, requirementsModel):
        '''
        For each goal including the oldObjectString, replace such string with newObjectString
        '''
        goalsDict = requirementsModel.searchGoalsBySubstring(self.oldObjectString)
        for goalID in goalsDict.keys():
            newName =  goalsDict[goalID].replace(self.oldObjectString, self.newObjectString)
            requirementsModel.changeGoalName(goalID, newName)

r = RequirementsModel("./models/ingolfo2011nomos.xml","/models/ingolfo2011nomos.xml")
t = ObjectChangeTransformation('health care','fitness')
t.transform(r)
r.saveModelAs('./models/ingolfo2011nomosCHANGED.xml')