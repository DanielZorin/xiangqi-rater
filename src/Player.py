'''
Created on 28.09.2011

@author: juan
'''

class Player(object):
    '''
    classdocs
    '''
    name = ""
    
    # default rating
    rating = 1200

    def __init__(self, name):
        '''
        Constructor
        '''
        self.name = name