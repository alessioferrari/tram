'''
Created on Jan 16, 2014

@author: alessioferrari
'''

class ModelIndex(object):
    '''
    This class is an inverted index for RequiremensModels.
    Given a keyword, returns all the RequirementsModels that contain 
    the keyword. Currently, the index stores all the models 
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        