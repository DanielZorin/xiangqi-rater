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
    rating = 1600
    
    foreign = False

    def __init__(self, name):
        '''
        Constructor
        '''
        self.name = name
        
    def __str__(self):
        return self.name + " " + str(self.rating)
    
    def shortName(self):
        return self.name[self.name.find(" ") + 1:] + " " + self.name[0]