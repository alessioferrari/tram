'''
Created on Jan 22, 2014

@author: alessioferrari
'''
from ModelIndexManager import ModelIndexManager
from ModelTransformer import ModelTransformer
from QueryManager import QueryManager
from RequirementsModelLoader import RequirementsModelLoader

class UserManager(object):
    '''
    This class implements the interaction with the user.
    It searches for the models within the DB, and applies the transformations. 
    '''


    def __init__(self, queryManager, modelTransformer):
        '''
        Constructor
        @param queryManager: a QueryManager object to perform the queries
        '''
        self.queryManager = queryManager
        self.modelTransformer = modelTransformer
        
    def run(self):
        '''
        This method embeds a sort of "main" function
        '''
        userString = "book shop"
        queryResult = self.queryManager.issueQuery(userString)

        oneResult = queryResult['shop'][0]
        self.modelTransformer.transform(oneResult[0],oneResult[1], {'oldObjectString':'item', 'newObjectString':'DVD'})
        print "done"
        
        

f = RequirementsModelLoader('./models')  
modelIndexManager = ModelIndexManager(f)        
q = QueryManager(modelIndexManager)
m = ModelTransformer(f)
u = UserManager(q, m)
u.run()