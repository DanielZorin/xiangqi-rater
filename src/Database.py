# -*- coding: cp1251 -*-
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
                    # TODO: rename tournament to smth
                    if tournament.nodeName == "player":
                        name = tournament.getAttribute("name")
                        rating = int(tournament.getAttribute("rating"))
                        p = Player(name)
                        p.rating = rating
                        p.foreign = True
                        self.players.append(p)
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
        self.tournaments = sorted(self.tournaments, key=lambda x:x.year)

    def FindGames(self, p1=None, p2=None):
        return [game for t in self.tournaments for game in t.games if 
                (game.red == p1 or game.red == p2) and (game.black == p1 or game.black == p2)]

    def PrintPairStats(self, p1, p2):
        games = self.FindGames(p1, p2)
        win = 0
        draw = 0
        lose = 0
        for g in games:
            if g.result == 0.5:
                draw += 1
            if g.result == 1:
                if g.red == p1:
                    win += 1
                else:
                    lose += 1
            if g.result == 0:
                if g.red == p2:
                    win += 1
                else:
                    lose += 1
        print(p1.name, p2.name, win, draw, lose)

    def PrintStats(self, cutoff):
        tmp = sorted(self.players, key=lambda x: -x.rating)
        tmp = [p for p in tmp if not p.foreign]
        for p1 in tmp[:cutoff]:
            for p2 in tmp[:cutoff]:
                if p1 != p2:
                    self.PrintPairStats(p1, p2)   
        
    def ComputeRating(self):
        year = self.tournaments[0].year
        while True:
            tourn = [x for x in self.tournaments if x.year == year]
            if tourn == []:
                return
            currentPlayers = {}
            for t in tourn:
                for g in t.games:
                    if g.black.name == "!bye":
                        # Ignore default wins
                        continue
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
                expScore = sum(1/(1+10**((other.rating - p.rating)/400)) for other in currentPlayers[p][1])
                realScore = currentPlayers[p][0]
                dif = realScore - expScore
                new = p.rating + 25 * dif
                if p.name == "Даниил Зорин":
                    print(year, expScore, realScore, p.rating, new)
                #if not p.foreign:
                #    print(t.name, p.name, expScore, realScore, p.rating, new)
                newRating[p] = new
            for p in newRating:
                p.rating = newRating[p]
            year += 1

db = Database()
db.loadFromXml("tournaments.xml")
db.ComputeRating()
tmp = sorted(db.players, key=lambda x: -x.rating)
tmp = [p for p in tmp if not p.foreign]
for p in tmp:
    if not p.foreign:
        print(p.name, p.rating)
cutoff = 6
db.PrintStats(cutoff)