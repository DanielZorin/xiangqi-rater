'''
Created on 28.09.2011

@author: juan
'''
from Player import Player

class Game:
    def __init__(self, p1, p2, result, tour=1):
        self.red = p1
        self.black = p2
        self.result = result
        self.tour = tour