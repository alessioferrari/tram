'''
Created on Jan 16, 2014

@author: alessioferrari
'''

from irutils.TextFilter import TextFilter
from nltk.tokenize.treebank import TreebankWordTokenizer
import sys
import xml.etree.ElementTree as ET

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
        
        self.tree =  ET.parse(self.path)
        
        self.modelGoals = self.__loadModelGoals()
        self.modelWords = self.__loadModelWords()
        self.modelStems = self.__loadModelStems()
        
    def __loadModelGoals(self):
        '''
        The function loads the goal names included in the model
        and returns a list with all the goals of the model.
        The goals names are stored as lowercase goals
        '''  
        root = self.tree.getroot()
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
    
    def loadModelSubtreeNames(self):
        '''
        The function scans the part of the XML file where we have GROUPS.
        When we find a group, we shall find also the names of any node 
        that is not a leaf: each node that is not a leaf is the head 
        of a subtree. The function stores the names of all the subtree roots,
        together with the ID of the subtree root (i.e., the id of the goal).
        
        @todo: we shall consider to use a threshold for the depth that
        we consider adequate for considering a sub-tree as a function. For example, if 
        the distance to a leaf is lower than 2, the node might not be a function
        '''
        root = self.tree.getroot()
        for group in root.iter('GROUP'):
            for e in group.iter('ENTITY'): #a left-depth first visit is performed to get the names
                print e.attrib['name']
            print '\n'
        
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

#r = RequirementsModel("ingolfo2011nomos.xml","ingolfo2011nomos.xml")
#r.loadModelSubtreeNames()