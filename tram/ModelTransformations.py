'''
Created on Jan 20, 2014

@author: alessioferrari

This file includes all the Transformations.
After a transformation is applied to a model, by calling the method
transform, the model has to be saved by calling savemodelAs,
in order not to change the original model.
'''
from RequirementsModel import RequirementsModel
import re

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
        For each goal including the oldObjectString, replace such a string 
        and all the case-insensitive occurrences of oldObjectString 
        with newObjectString
        '''
        goalsDict = requirementsModel.searchGoalsBySubstring(self.oldObjectString)
        for goalID in goalsDict.keys():
            insensitiveOldObjectString = re.compile(re.escape(self.oldObjectString), re.IGNORECASE)
            newName = insensitiveOldObjectString.sub(self.newObjectString, goalsDict[goalID])
            requirementsModel.changeGoalName(goalID, newName)


class FunctionalityExtension(object):
    '''
    This class is a transformation that transform a RequirementsModel into another
    by adding a functionality
    '''
    
    def __init__(self, functionalityObject, nodeID):
        '''
        Constructor
        '''
        self.functionalityObject = functionalityObject
        self.nodeID = nodeID

    def transform(self, requirementsModel):
        '''
        The function searches for the nodeObject within the model.
        Then, it adds the @param functionalityObject as a child of the
        node that has nodeID as identifier
        '''
        
        
#r = RequirementsModel("./models/ingolfo2011nomos.xml","/models/ingolfo2011nomos.xml")
#t = ObjectChangeTransformation('health care','fitness')
#t.transform(r)
#r.saveModelAs('./models/ingolfo2011nomosCHANGED.xml')