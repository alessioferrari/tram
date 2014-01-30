'''
Created on Jan 30, 2014

@author: alessioferrari
'''

class QueryResult(list):
    '''
    This class embeds the result of a query.
    It stores the specification query, together
    with models and recommended transformations.
    
    More specifically, this class embeds an ordered list of couples (item, score)
    where (item) is a tuple (modelpath, modelname, transformationlist) and transformationlist
    is a list of transformation.
    The list is reversed since the we show the models starting from the one that has the highest score
    '''


    def __init__(self, specificationQuery=""):
        '''
        Constructor
        '''
        
        self.specificationQuery = specificationQuery
        
    def addItem(self, modelpath, model, transformationList, score = 0.0):
        '''
        This function adds an item to the list of results
        @param model: this is a string representing the model
        @param transformationList: this is a list of strings that represent the transformations
        to be applied to the model
        @param score: this is a score to be applied to the item
        '''
        item = (modelpath, model, transformationList)
        self.append((item, score))
        self.sort(key=lambda score: score[1])
        self.reverse()
        
    def getModelPath(self, id):
        '''
        Given the id of a result (i.e., its position in the list), returns the path to the model,
        which is in position [id][0][0] 
        '''    
        return self[id][0][0]
    
        
        