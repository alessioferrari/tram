'''
Created on Feb 3, 2014

@author: alessioferrari
'''

class QueryResult(object):
    '''
    Simple class that stores the single result of a query
    '''


    def __init__(self, modelInfo, transformationList, score):
        '''
        Constructor
        '''
        self.modelInfo = modelInfo
        self.transformationList = transformationList
        self.score = score
        
    def getModelInfo(self):
        
        return self.modelInfo
    
    def getTransformationList(self):
        return self.transformationList
    
    def getScore(self):
        return self.score