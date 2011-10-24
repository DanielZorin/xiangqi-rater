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

    rated = True

    def __init__(self, games, date, name=""):
        '''
        Constructor
        '''
        self.games = games
        self.date = date
        tmp = date.split(".")
        self.year = int(tmp[2])
        self.name = name

    def FindGames(self, p1=None, p2=None):
        return [game for game in self.games if 
                (p2 == None) and (game.red == p1 or game.black == p1) or
                ((game.red == p1 or game.red == p2) and (game.black == p1 or game.black == p2))]

    # TODO: fix
    def cmp2key(self, mycmp):
        'Convert a cmp= function into a key= function'
        class K(object):
            def __init__(self, obj, *args):
                self.obj = obj
            def __lt__(self, other):
                return mycmp(self.obj, other.obj) < 0
            def __gt__(self, other):
                return mycmp(self.obj, other.obj) > 0
            def __eq__(self, other):
                return mycmp(self.obj, other.obj) == 0
            def __le__(self, other):
                return mycmp(self.obj, other.obj) <= 0
            def __ge__(self, other):
                return mycmp(self.obj, other.obj) >= 0
            def __ne__(self, other):
                return mycmp(self.obj, other.obj) != 0
        return K
        
    def findPlaces(self):
        def compareResults(r1, r2):
            if r1[1] > r2[1]:
                return -1
            elif r1[1] < r2[1]:
                return 1
            else:
                if r1[2] > r2[2]:
                    return -1
                elif r1[2] < r2[2]:
                    return 1
                else:
                    #Buchholz coefficients
                    g1 = self.FindGames(r1[0])
                    g2 = self.FindGames(r2[0])
                    buch1 = 0
                    buch2 = 0
                    
                    # weighted coefficients
                    buchw1 = 0
                    buchw2 = 0
                    for g in g1:
                        other = g.red if g.red != r1[0] else g.black
                        if other.name != "!bye":
                            buch1 += self.places[other][0]
                            if g.winner() == r1[0]:
                                buchw1 += self.places[other][0]
                            if g.result == 0.5:
                                buchw1 += self.places[other][0] / 2
                    for g in g2:
                        other = g.red if g.red != r2[0] else g.black
                        if other.name != "!bye":
                            buch2 += self.places[other][0]
                            if g.winner() == r2[0]:
                                buchw2 += self.places[other][0]
                            if g.result == 0.5:
                                buchw2 += self.places[other][0] / 2
                            
                    if buch1 > buch2:
                        return -1
                    elif buch1 < buch2:
                        return 1
                    else:
                        return -1 if buchw1 > buchw2 else 1
        self.places = {}
        for g in self.games:
            if not g.red in self.places.keys():
                self.places[g.red] = [0, 0]
            if not g.black in self.places.keys():
                self.places[g.black] = [0, 0]
            if g.result == 1:
                self.places[g.red][0] += 1
                if g.black.name != "!bye":
                    self.places[g.red][1] += 1
            elif g.result == 0:
                self.places[g.black][0] += 1
                self.places[g.black][1] += 1
            else:
                self.places[g.red][0] += 0.5
                self.places[g.black][0] += 0.5
                self.places[g.red][1] += 0.5
                self.places[g.black][1] += 0.5
        results = []
        for p in self.places.keys():
            results.append([p, self.places[p][0], self.places[p][1]])
        results = sorted(results, key=self.cmp2key(compareResults))
        self.places = []
        i = 1
        for r in results:
            #print(self.name, r[0].name, r[1], r[2])
            self.places.append([i, r[0], r[1], r[2]])
            i += 1