'''
Created on Jan 16, 2014

@author: alessioferrari
'''

from ModelInfo import ModelInfo
from irutils.TextFilter import TextFilter
from nltk.tokenize.treebank import TreebankWordTokenizer
from xml.etree.ElementTree import ElementTree, Element
import sys
import xml.etree.ElementTree as ET

'''
These are the constants to distinguish the different types of information
that can be used from the model, for example to build the index
'''
STEM_STRING = "STEM"
WORD_STRING = "WORD"
GOAL_STRING = "GOAL"

'''
This is the separator for objects in the XML file
'''
OBJ_SEPARATOR = ", "

class RequirementsModel(object):
    '''
    This class embeds the information residing in the XML
    of a requirements model passed as input parameter
    during construction 
    '''

    def __init__(self, modelID, inputXMLfilepath= "", modelType="", title="", objects=[]):
        '''
        Constructor
        @param modelID: identifier of the model
        @param inputXMLfilepath: path to the input XML file containing the model 
        if this parameter is left empty a new XML tree is created
        @param type: KAOS, TROPOS, or any other kind of model
        '''
        self.textFilter = TextFilter()
        self.wordTokenizer = TreebankWordTokenizer()        
        self.maxID = "100"  #@todo: we have to set the current maximum to the actual maximum value
                            #for the model
        self.modelInfo = ModelInfo(modelID)
        
        if not inputXMLfilepath == "":
            
            self.modelInfo.setLocation(inputXMLfilepath)
            
            self.tree =  ET.parse(self.modelInfo.getLocation())
        
            self.__loadModelInfo(self.modelInfo)
            self.modelGoals = self.__loadModelGoals()
            self.modelWords = self.__loadModelWords()
            self.modelStems = self.__loadModelStems()
        else:
            attributes = dict()
            attributes['type'] = modelType
            attributes['title'] = title
            attributes['object'] = objects
            root = Element("MODEL", attributes)
            self.tree = ElementTree(root)
    
    def __loadModelInfo(self, modelInfo):
        '''
        This function load the name of the model from the "title" field of the MODEL tag,
        together with the type and the objects, and stores these information in the 
        ModelInfo object
        '''
        root = self.tree.getroot()
        
        modelInfo.setName(self.textFilter.lower_all(root.get("title")))
        modelInfo.setType(self.textFilter.lower_all(root.get("type")))
        
        objects = root.get("object").strip().split(OBJ_SEPARATOR)
        lowercaseObjects = [self.textFilter.lower_all(o) for o in objects]
        modelInfo.setObjects(lowercaseObjects)   
    
    
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
        
    def __getModelStems(self):
        return self.modelStems.keys()
    
    def __getModelWords(self):
        return self.modelWords.keys()
    
    def __getModelGoals(self):
        return self.modelGoals
    
    def getModelInfo(self):
        return self.modelInfo
    
    def getModelID(self):
        return self.modelInfo.getId()
    
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
    
    def __assignUniqueIDs(self, treeRoot):
        '''
        This function assigns unique IDs to all the objects 
        of type ENTITY in @param tree
        '''
        currentMaxId = self.maxID
        for child in treeRoot.iter('ENTITY'):
            currentMaxId = str( int(currentMaxId) + 1 )
            child.attrib['id'] = currentMaxId
            
        self.maxID = currentMaxId
    
    def insertTree(self, parentID, childTree):
        '''
        Given a @param childTree, which is a tree or a node, this is added as a child of parentID
        below the first refinement of the parent. 
        The assumption here is that each parent can have ONLY ONE TYPE of refinement.
        The unique IDs to the child elements are dynamically assigned by the function. 
        The childTree could be also a single node.
        '''
        root = self.tree.getroot()
        
        for child in root.iter('ENTITY'):
            if child.attrib['id'] == parentID:
                refinement = child.findall("REFINEMENT")
                if refinement and len(refinement) == 1: #ONLY ONE TYPE of refinement is allowed for each element
                    self.__assignUniqueIDs(childTree)
                    refinement[0].append(childTree)
                    return

    def saveModelAs(self, destinationFilePath):
        '''
        @param destinationFilePath: path of the file where the model shall be saved.
        @todo: currently the model is saved to another location and the original location
        is lost. Therefore, the model currently keeps the same ID. We have to change
        this behaviour. 
        '''
        self.modelInfo.setLocation(destinationFilePath) 
        self.saveModel()
        
    def saveModel(self):
        '''
        Save the model in the same destination as the input folder
        and with the original name
        '''
        try:
            self.tree.write(self.modelInfo.getLocation())
        except IOError:
            print "IOError: Saving to a path that does not exist! Use saveModelAs() instead"
        except:
            print "An error occurred"

#TEST
#r = RequirementsModel("./models/ingolfo2011nomos.xml","./models/ingolfo2011nomos.xml")
#goalID = r.searchGoalByName('Access health care centre')
#attributes = dict()
#attributes['id'] = ''
#attributes['name'] = 'New Goal'
#attributes['type'] = 'goal'
#newElement = Element("ENTITY", attributes)
#newElement.append(Element("ENTITY", {'type': 'goal', 'name': 'ChildGoal'}))
#r.insertTree(goalID, newElement)
#
#r.saveModelAs('./models/ingolfo2011nomosCHANGED.xml')

#TEST
#r = RequirementsModel("./models/morales2011technology.xml","./models/morales2011technology.xml")
#i = r.getModelInfo()
#print i.getName(), i.getLocation(), i.getType(), i.getObjects() 
       