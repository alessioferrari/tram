'''
Created on Jan 16, 2014

@author: alessioferrari
'''
from ModelIndexManager import ModelIndexManager
from QueryResult import QueryResult
from RequirementsModel import STEM_STRING
from RequirementsModelLoader import RequirementsModelLoader
from irutils.TextFilter import TextFilter
from nltk.tokenize.treebank import TreebankWordTokenizer

class QueryManager(object):
    '''
    Given a specification query, this object returns a set of models
    together with possible transformations that can be applied to the model
    to address the satisfy the specification query
    '''


    def __init__(self, modelIndexManager):
        '''
        @param modelIndex: reference to the place where the models are indexed
        '''
        self.textFilter = TextFilter()
        self.modelIndexManager = modelIndexManager
        self.wordTokenizer = TreebankWordTokenizer()
        
    def __parseQuery(self, queryString):
        '''
        This function returns the words included in queryString,
        after filtering all the stopwords, performing stemmming
        and applying all the filters provided by textFilter
        @param queryString: the specification query in the form of a string 
        ''' 
        filteredQueryString = self.textFilter.filter_all(queryString)
        return self.wordTokenizer.tokenize(filteredQueryString)
        
    def issueQuery(self, queryString):
        '''
        This is the main function of this class. Given the specification
        query, the function parses the specification and returns a
        set of QueryResult objects, which include the link to the models
        @param queryString: the specification query in the form of a string
        @return: a dictionary of QueryResult objects.
        '''
        #results = dict()
        
        qr = list()
        
        stems = self.__parseQuery(queryString)
        for stem in stems:
            #modelsTransformationsList = list()
            
            modelsInfos = self.modelIndexManager.searchModels(stem, STEM_STRING)
            
            #modelsTransformationsList = [(model, "object change") for model in models]
            #results[stem] = modelsTransformationsList
        
            if not modelsInfos == None:
                for modelInfo in modelsInfos:
                    score = 0.1
                    qr.append(QueryResult(modelInfo, ['object change'], score))
                    
            qr.sort(key=lambda x: x.score) #the list is ordered by the score attribute and reversed
            qr.reverse()
        
        '''
        @todo: for each model we shall understand which is the best transformation.
        To this end, an additional class is required.
        Currently, we always add the object change transformation together 
        with each model found. 
        '''
        
        return qr   

#TEST
#f = RequirementsModelLoader('./models')  
#modelIndexManager = ModelIndexManager(f)        
#q = QueryManager(modelIndexManager)
#print q.issueQuery("book shop")
