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
#        root = self.tree.getroot()
#        for group in root.iter('GROUP'):
#            for e in group.iter('ENTITY'): #a left-depth first visit is performed to get the names
#                print e.attrib['name']
#            print '\n'
        
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
        
    def changeGoalName(self, goalID, newGoalName):
        '''
        @param goalID: ID of the goal that shall have a new name
        @param newGoalName: string representing the new name of the goal  
        '''
        root = self.tree.getroot()

        for child in root.iter('ENTITY'):
            if child.attrib['type'] == 'goal' and child.attrib['id'] == goalID:
                child.attrib['name'] = newGoalName 
        
    def searchGoalByName(self, goalName):
        '''
        @param goalName: name of the goal to be searched
        return: goalID, which is the unique ID of the goal, if the goal exist
                -1, if the goal is not found
        '''
        root = self.tree.getroot()

        for child in root.iter('ENTITY'):
            if child.attrib['type'] == 'goal' and child.attrib['name'] == goalName:
                return child.attrib['id']
        
        return -1 
    
    def searchGoalsBySubstring(self, goalSubstring, caseSensitive = "NO"):
        '''
        @param goalSubstring: a substring that shall be searched among the goal names. 
        By default the search is not case sensitive
        return: a list with the couples [ID, goalName] of the goals that include the @param goalSubstring
        '''
        root = self.tree.getroot()
        goalDict = dict()

        for child in root.iter('ENTITY'):
            if child.attrib['type'] == 'goal': 
                if caseSensitive == "NO":
                    if self.textFilter.lower_all(goalSubstring) in self.textFilter.lower_all(child.attrib['name']):
                        goalDict[child.attrib['id']] = child.attrib['name']
                else:
                    if goalSubstring in child.attrib['name']:
                        goalDict[child.attrib['id']] = child.attrib['name']
                
        
        return goalDict

    def saveModelAs(self, destinationFilePath):
        '''
        @param destinationFilePath: path of the file where the model shall be saved 
        '''
        self.path = destinationFilePath
        self.saveModel()
        
    def saveModel(self):
        '''
        Save the model in the same destination as the input folder
        and with the original name
        '''
        self.tree.write(self.path)

#r = RequirementsModel("./models/ingolfo2011nomos.xml","/models/ingolfo2011nomos.xml")
#goalID = r.searchGoalByName('Access health care centre')
#print r.searchGoalsBySubstring('health')

#r.changeGoalName(goalID, 'Changed goal name')
#r.saveModelAs('./models/ingolfo2011nomosCHANGED.xml')
#r.saveModel()


