'''
Created on Jan 16, 2014

@author: alessioferrari
'''

from irutils.TextFilter import TextFilter
import sys
import xml.etree.ElementTree as ET
from nltk.tokenize.treebank import TreebankWordTokenizer

'''
These are the constants to distinguish the different types of information
that can be used from the model, for example to build the index
'''
STEM_STRING = "STEM"
WORD_STRING = "WORD"
GOAL_STRING = "GOAL"

class RequirementsModel(object):
    '''
    This class embeds the information residing in the XML
    of a requirements model passed as input parameter
    during construction 
    '''

    def __init__(self, inputXMLfilepath, modelID):
        '''
        Constructor
        @param inputXMLfilepath: path to the input XML file containing the model 
        '''
        self.path = inputXMLfilepath
        self.modelID = modelID
        self.textFilter = TextFilter()
        self.wordTokenizer = TreebankWordTokenizer()
        
        self.modelGoals = self.__loadModelGoals()
        self.modelWords = self.__loadModelWords()
        self.modelStems = self.__loadModelStems()
        
    def __loadModelGoals(self):
        '''
        The function loads the goal names included in the model
        and returns a list with all the goals of the model.
        The goals names are stored as lowercase goals
        ''' 
        tree = ET.parse(self.path)
        root = tree.getroot()
        goalNames = list()

        for child in root.iter('ENTITY'):
            if child.attrib['type'] == 'goal': 
                goalNames.append(self.textFilter.lower_all(child.attrib['name'])) 
                    
        return goalNames
        
        
    def __loadModelWords(self):
        '''
        The function loads the words included in the model
        and returns a dictionary with all the words of the model
        and their frequency
        '''
               
        tokenizedWords = dict()

        if not self.modelGoals == None:
            for name in self.modelGoals:
                nameFiltered = self.textFilter.filter_all_except_stem(name)
                words = self.wordTokenizer.tokenize(nameFiltered)
                for word in words:
                    if not tokenizedWords.has_key(word): 
                        tokenizedWords[word] = 1
                    else:
                        tokenizedWords[word] = tokenizedWords[word] + 1
                    
        return tokenizedWords
        
    def __loadModelStems(self):
        '''
        The function loads the stems included in the model
        and returns a dictionary with all the stems of the model
        and their frequency
        ''' 
        tokenizedStems = dict()
        
        if not self.modelWords == None:
            for w in self.modelWords:
                stem = self.textFilter.filter_all(w)
                if not tokenizedStems.has_key(stem):
                    tokenizedStems[stem] = 1
                else:
                    tokenizedStems[stem] = tokenizedStems[stem] + 1
                    
        return tokenizedStems
            
        
    def __getModelStems(self):
        return self.modelStems.keys()
    
    def __getModelWords(self):
        return self.modelWords.keys()
    
    def __getModelGoals(self):
        return self.modelGoals
    
    def getModelID(self):
        return self.modelID
    
    def getModelKeys(self, keyType):
        if keyType == STEM_STRING:
            return self.__getModelStems()
        if keyType == WORD_STRING:
            return self.__getModelWords()
        if keyType == GOAL_STRING:
            return self.__getModelGoals()
