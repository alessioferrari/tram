'''
Created on Jan 17, 2014

@author: alessioferrari
'''
from ModelIndex import ModelIndex
from RequirementsModel import WORD_STRING, STEM_STRING, GOAL_STRING

class ModelIndexManager(object):
    '''
    This class stores a set of ModelIndexes and calls one index or the 
    other according to the type of query that is issued
    '''


    def __init__(self, requirementsModelLoader):
        '''
        Constructor
        '''
        self.wordIndex = ModelIndex(requirementsModelLoader, WORD_STRING)
        self.stemIndex = ModelIndex(requirementsModelLoader, STEM_STRING)
        self.goalIndex = ModelIndex(requirementsModelLoader, GOAL_STRING)
        
    def searchModels(self, keyword, searchType = STEM_STRING):
        if searchType == STEM_STRING:
            return self.stemIndex.searchModels(keyword)
        if searchType == WORD_STRING:
            return self.wordIndex.searchModels(keyword)
        if searchType == GOAL_STRING:
            return self.goalIndex.searchModels(keyword)