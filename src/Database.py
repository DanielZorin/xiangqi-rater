'''
Created on 28.09.2011

@author: juan
'''
from Tournament import Tournament
from Game import Game
from Player import Player
import xml.dom.minidom

class Database(object):

    def __init__(self):
        '''
        Constructor
        '''
        self.tournaments = []
        self.players = []
       
    def findPlayer(self, name):
        try:
            res = next((p for p in self.players if p.name == name))
            return res
        except StopIteration:
            return None
        
    def loadFromXml(self, filename):
        f = open(filename, "r")
        dom = xml.dom.minidom.parse(f)
    
        for node in dom.childNodes:
            if node.tagName == "xiangqi":
                #Parse vertices
                for tournament in node.childNodes:
                    if tournament.nodeName == "tournament":
                        games = []
                        for game in tournament.childNodes:
                            if game.nodeName == "game":
                                red = game.getAttribute("red")
                                black = game.getAttribute("black")
                                res = float(game.getAttribute("result"))
                                tour = int(game.getAttribute("tour"))
                                tmp = self.findPlayer(red)
                                if tmp:
                                    red = tmp
                                else:
                                    red = Player(red)
                                    self.players.append(red)
                                tmp = self.findPlayer(black)
                                if tmp:
                                    black = tmp
                                else:
                                    black = Player(black)
                                    self.players.append(black)
                             
                                g = Game(red, black, res, tour)
                                games.append(g)                              
                        date = tournament.getAttribute("date")
                        name = tournament.getAttribute("name")
                        t = Tournament(games, date, name)
        f.close()
        
    def ComputeRating(self):
        pass
        
db = Database()
db.loadFromXml("tournaments.xml")
for p in db.players:
    print(p.name, p.rating)