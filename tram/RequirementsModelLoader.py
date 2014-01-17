'''
Created on Jan 17, 2014

@author: alessioferrari
'''
from RequirementsModel import RequirementsModel
import os

class RequirementsModelLoader(object):
    '''
    This class creates all the RequirementsModel objects residing in a directory
    '''


    def __init__(self, modelDirectory):
        '''
        Constructor
        '''
        self.requirementsModelList = list()
        
        os.chdir(modelDirectory)
        for dirFile in os.listdir("."):
            if dirFile.endswith(".xml"):  
                requirementsModel = RequirementsModel(dirFile, dirFile)
                self.requirementsModelList.append(requirementsModel) 
                
    def getModels(self):
        "Returns a list to all the models stored in the directory"
        return self.requirementsModelList