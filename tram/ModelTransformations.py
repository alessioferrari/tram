'''
Created on Jan 20, 2014

@author: alessioferrari

This file includes all the Transformations.
After a transformation is applied to a model, by calling the method
transform, the model has to be saved by calling savemodelAs,
in order not to change the original model.
'''
from RequirementsModel import RequirementsModel, FunctionalityModel
from xml.etree.ElementTree import Element
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

#TEST        
#r = RequirementsModel("./models/ingolfo2011nomos.xml","/models/ingolfo2011nomos.xml")
#t = ObjectChangeTransformation('health care','fitness')
#t.transform(r)
#r.saveModelAs('./models/ingolfo2011nomosCHANGED.xml')


class FunctionalityExtension(object):
    '''
    This class is a transformation that transform a RequirementsModel into another
    by adding a functionality
    '''
    
    def __init__(self, functionalityModel, nodeName):
        '''
        Constructor
        @functionalityModel: this is a model of a functionality, whose sub-elements
        are stored in a tree-like structure
        @nodeName: node where we wish to attach our functionalityModel
        '''
        self.functionalityModel = functionalityModel
        self.nodeName = nodeName

    def transform(self, requirementsModel):
        '''
        The function searches for the nodeObject with nodeID within the model.
        Then, it adds the @param functionalityModel as a child of the
        node that has nodeID as identifier
        '''
        goalID = requirementsModel.searchGoalByName(self.nodeName)
        functionalityNode = self.functionalityModel.getFunctionalityNode()
        requirementsModel.insertTree(goalID, functionalityNode)
        
r = RequirementsModel("./models/ingolfo2011nomos.xml","./models/ingolfo2011nomos.xml")
f = FunctionalityModel('myfunctionality')


#goalID = r.searchGoalByName('Access health care centre')
#attributes = dict()
#attributes['id'] = ''
#attributes['name'] = 'New Goal'
#attributes['type'] = 'goal'
#newElement = Element("ENTITY", attributes)
#newElement.append(Element("ENTITY", {'type': 'goal', 'name': 'ChildGoal'}))
#f.insertTree(goalID, newElement)
