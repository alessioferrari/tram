'''
Created on Feb 4, 2014

@author: alessioferrari
'''
from ModelInfo import ModelInfo
from ModelTransformer import OBJECT_CHANGE
from irutils.TextFilter import TextFilter
from nltk.tokenize.treebank import TreebankWordTokenizer



class TransformationRecommender(object):
    '''
    This class recommends a transformation according
    to the model information ModelInfo object and the query issued
    '''
    
    '''
    This object is a Singleton, since it does not have private data
    but only functions: the code below defines a singleton
    '''
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TransformationRecommender, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        self.tf = TextFilter()
        self.wordTokenizer = TreebankWordTokenizer()

    def getRecommendedTransformation(self, modelInfo, query):
        '''
        If the input sentence is the same as the title except than in the title
        part that specifies the object, then "object change" shall be suggested
        '''
        title = modelInfo.getName()
        titleFiltered = self.tf.filter_all_except_stem(title)
        titleToks = self.wordTokenizer.tokenize(titleFiltered)
        
        titleToksNoObj = [t for t in titleToks if t not in modelInfo.getObjects()]
        
        queryFiltered = self.tf.filter_all_except_stem(query)
        sentenceToks = self.wordTokenizer.tokenize(queryFiltered)
        
        if set(titleToksNoObj).issubset(sentenceToks):
            return OBJECT_CHANGE
        else:
            return ''
            
        
        
        
        
#t = TransformationRecommender()
#t.getRecommendedTransformation(ModelInfo('32', name="car system", location="x", modelType="x", objects=['car']), 'bus system')
        
        
    