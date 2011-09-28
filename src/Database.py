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
                        self.tournaments.append(t)
        f.close()
        
    def ComputeRating(self):
        for t in self.tournaments:
            currentPlayers = {}
            for g in t.games:
                if not g.red in currentPlayers:
                    currentPlayers[g.red] = (g.result, [g.black])
                else:
                    tmp = currentPlayers[g.red]
                    currentPlayers[g.red] = (tmp[0] + g.result, tmp[1] + [g.black])
                if not g.black in currentPlayers:
                    currentPlayers[g.black] = (1 - g.result, [g.red])
                else:
                    tmp = currentPlayers[g.black]
                    currentPlayers[g.black] = (tmp[0] + 1 - g.result, tmp[1] + [g.red])
            newRating = {}
            for p in currentPlayers.keys():
                expScore = sum(1/(1+10**((p.rating - other.rating)/400)) for other in currentPlayers[p][1])
                realScore = currentPlayers[p][0]
                dif = realScore - expScore
                new = p.rating + 10 * dif
                newRating[p] = new
            for p in newRating:
                p.rating = newRating[p]
        
db = Database()
db.loadFromXml("tournaments.xml")
db.ComputeRating()
for p in db.players:
    print(p.name, p.rating)