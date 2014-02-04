'''
Created on Jan 20, 2014

@author: alessioferrari
'''
from ModelTransformations import ObjectChangeTransformation
OBJECT_CHANGE = "object change"

class ModelTransformer(object):
    '''
    This class transforms a model into another according to the 
    required transformation. The class is also in charge 
    of saving the model after transforming it.
    '''


    def __init__(self, requirementsModelLoader):
        '''
        Constructor
        @param requirementsModelLoader: the class that gives a reference to the models 
        '''
        self.requirementsModelLoader = requirementsModelLoader
        
    def transform(self, modelID, transformationString, transformationPars):
        '''
        @param modelID: ID of the RequirementsModel
        @param transformationString: Id associated to the ModelTransformation
        @param transformationPars: parameters of the transformation stored in a dictionary 
        '''
        if transformationString == OBJECT_CHANGE:
            t = ObjectChangeTransformation(transformationPars['oldObjectString'], transformationPars['newObjectString'])
            requirementsModel = self.requirementsModelLoader.getModel(modelID)
            t.transform(requirementsModel)
            requirementsModel.saveModelAs('CHANGED1.xml')
            print "model has been transformed"