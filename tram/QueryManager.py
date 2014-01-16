'''
Created on Jan 16, 2014

@author: alessioferrari
'''
from ModelIndex import ModelIndex
from irutils.TextFilter import TextFilter
from nltk.tokenize.treebank import TreebankWordTokenizer

class QueryManager(object):
    '''
    Given a specification query, this object returns a set of models
    together with possible transformations that can be applied to the model
    to address the satisfy the specification query
    '''


    def __init__(self, modelIndex):
        '''
        @param modelIndex: reference to the place where the models are indexed
        '''
        self.textFilter = TextFilter()
        self.modelIndex = modelIndex
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
        @return: a list of QueryResult objects.
        '''
        words = self.__parseQuery(queryString)
        for w in words:
            models = self.modelIndex.searchModels(w)
            print w, models
        
m = ModelIndex('./')        
q = QueryManager(m)
q.issueQuery("receive access retrieve authority")
