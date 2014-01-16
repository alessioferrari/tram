'''
Created on Jan 16, 2014

@author: alessioferrari
'''

class RequirementsModel(object):
    '''
    This class embeds the information residing in the XML
    of a requirements model passed as input parameter
    during construction 
    '''

    def __init__(self, inputXMLfilepath):
        '''
        Constructor
        @param inputXMLfilepath: path to the input XML file containing the model 
        '''
        