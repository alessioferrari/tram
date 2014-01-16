'''
Created on Jan 16, 2014

@author: alessioferrari
'''

class QueryManager(object):
    '''
    Given a specification query, this object returns a set of models
    together with possible transformations that can be applied to the model
    to address the satisfy the specification query
    '''


    def __init__(self, modelIndex):
        '''
        Constructor
        '''
        