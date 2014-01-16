'''
Created on Jan 16, 2014

@author: alessioferrari
'''

from irutils.TextFilter import TextFilter
import sys
import xml.etree.ElementTree as ET
from nltk.tokenize.treebank import TreebankWordTokenizer

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
        
        self.modelWords = self.__loadModelWords()
        
    def __loadModelWords(self):
        '''
        The function loads the words included in the model
        and returns a dictionary with all the words of the model
        and their frequency
        ''' 
        tree = ET.parse(self.path)
        root = tree.getroot()
        goalNames = list()

        for child in root.iter('ENTITY'):
            if child.attrib['type'] == 'goal': 
                goalNames.append(child.attrib['name']) 
               
        tokenizedWords = dict()

        for name in goalNames:
            nameFiltered = self.textFilter.filter_all(name)
            words = self.wordTokenizer.tokenize(nameFiltered)
            for word in words:
                if not tokenizedWords.has_key(word): 
                    tokenizedWords[word] = 1
                else:
                    tokenizedWords[word] = tokenizedWords[word] + 1
                    
        return tokenizedWords
        
    def getModelWords(self):
        return self.modelWords.keys()
    
    def getModelID(self):
        return self.modelID
