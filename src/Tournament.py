'''
Created on 28.09.2011

@author: juan
'''
from Game import Game
from Player import Player

class Tournament(object):
    '''
    classdocs
    '''

    def __init__(self, games, date, name=""):
        '''
        Constructor
        '''
        self.games = games
        self.date = date
        self.name = name