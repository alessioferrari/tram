'''
Created on Jan 16, 2014

@author: alessioferrari
'''
from RequirementsModel import RequirementsModel, STEM_STRING
from RequirementsModelLoader import RequirementsModelLoader




class ModelIndex(object):
    '''
    This class is an inverted index for RequiremensModels.
    Given a keyword, returns all the RequirementsModels that contain 
    the keyword. Currently, the index stores all the models 
    '''
    

    def __init__(self, requirementsModelLoader, indexType = STEM_STRING):
        '''
        Constructor.
        @param requirementsModelLoader: classes that stores all the models in memory
        '''
        self.indexType = indexType
        self.requirementsModelLoader = requirementsModelLoader
        self.dictionary = self.__buildIndex(self.requirementsModelLoader)
        
    
    def __addModel(self, modelInfo, modelKeys, dictionary):
        '''
        This function adds a model to a dictionary
        @param modelInfo: object identifying the model
        @param modelKeys: keywords or entire terms in the model
        @param dictionary: the dictionary   
        '''
        for modelKey in modelKeys:
            if not dictionary.has_key(modelKey):
                l = list()
                l.append(modelInfo) 
                dictionary[modelKey] = l
            else:
                dictionary[modelKey].append(modelInfo) 
    
    def __buildIndex(self, requirementsModelLoader):
        '''
        This function scans the models loaded in memory
        and builds the index. For each word found in a model, 
        the word is added to the dictionary. 
        If the entry for the word does not exist, a new entry is created.
        '''
        
        dictionary = dict()

        for requirementsModel in requirementsModelLoader.getModels():  
            modelInfo = requirementsModel.getModelInfo()
            modelKeys = requirementsModel.getModelKeys(self.indexType)
            self.__addModel(modelInfo, modelKeys, dictionary)
        
        return dictionary
    
    def searchModels(self, keyword):
        '''
        Given a keyword, searches for the models that contain such a keyword
        '''
        if self.dictionary.has_key(keyword):
            return self.dictionary[keyword]
        else: 
            return None

#TEST        
#f = RequirementsModelLoader('./models')        
#m = ModelIndex(f, "STEM")
#print m.searchModels('health')[0].getName()