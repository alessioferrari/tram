'''
Created on Feb 3, 2014

@author: alessioferrari
'''

class ModelInfo(object):
    '''
    This class includes the main information concerning
    the RequirementsModel
    '''


    def __init__(self, modelID, name="", location="", modelType="", objects=[]):
        '''
        The only required field is the ID, the other field of the class
        can be set up later
        '''
        self.modelID = modelID
        self.name = name
        self.location = location
        self.modelType = modelType
        self.objectList = list(objects) 
        
    def getId(self):
        return self.modelID
    
    def getName(self):
        return self.name
    
    def getLocation(self):
        return self.location
    
    def getType(self):
        return self.modelType
    
    def getObjects(self):
        return self.objectList
    
    def setLocation(self, location):
        self.location = location
    
    def setName(self, name):
        self.name = name 
        
    def setType(self, modelType):
        self.modelType = modelType
        
    def setObjects(self, objects):
        self.objectList = list(objects)