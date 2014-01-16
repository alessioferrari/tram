'''
Created on Jan 16, 2014

@author: alessioferrari
'''
from RequirementsModel import RequirementsModel
from os import path
import os

class ModelIndex(object):
    '''
    This class is an inverted index for RequiremensModels.
    Given a keyword, returns all the RequirementsModels that contain 
    the keyword. Currently, the index stores all the models 
    '''
    

    def __init__(self, modelDirectory):
        '''
        Constructor.
        @param modelDirectory: directory where the XML models are placed
        '''
        self.dictionary = self.__buildIndex(modelDirectory)
        
    
    def __addModel(self, modelId, modelWords, dictionary):
        '''
        This function adds a model to the dictionary
        @param modelId: unique string identifying the model
        @param modelWords: words in the model
        @param dictionary: the dictionary   
        '''
        for modelWord in modelWords:
            if not dictionary.has_key(modelWord):
                l = list()
                l.append(modelId) 
                dictionary[modelWord] = l
            else:
                dictionary[modelWord].append(modelId) 
    
    def __buildIndex(self, modelDirectory):
        '''
        This function scans the directory where the models are placed
        and build the index. For each word found in a model, 
        the word is added to the dictionary. 
        If the entry for the word does not exist, a new entry is created.
        '''
        
        dictionary = dict()

        os.chdir(modelDirectory)
        for dirFile in os.listdir("."):
            if dirFile.endswith(".xml"):  
                requirementsModel = RequirementsModel(dirFile, dirFile)
                modelId = requirementsModel.getModelID()
                modelWords = requirementsModel.getModelWords()
                self.__addModel(modelId, modelWords, dictionary)
        
        return dictionary
    
    def searchModels(self, keyword):
        '''
        Given a keyword, searches for the models that contain such a keyword
        '''
        if self.dictionary.has_key(keyword):
            return self.dictionary[keyword]
        else: 
            return None
        
        
#m = ModelIndex('./')
#m.searchModels('quot')