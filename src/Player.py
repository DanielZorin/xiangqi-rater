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
    rating = 1400
    
    foreign = False

    def __init__(self, name):
        '''
        Constructor
        '''
        self.name = name
        
    def __str__(self):
        return self.name + " " + self.rating