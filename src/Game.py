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
        self.tournament = None
    
    def setTournament(self, t):
        self.tournament = t

    def winner(self):
        if self.result == 1:
            return self.red
        elif self.result == 0:
            return self.black
        else:
            return None
        
    def __str__(self):
        res = "1-0" if self.result == 1 else "0.5-0.5" if self.result == 0.5 else "0-1"
        return self.red.name + " vs " + self.black.name + " " + res + " // " + self.tournament.name