# -*- coding: cp1251 -*-
'''
Created on 28.09.2011

@author: juan
'''
import xml.dom.minidom, math

class Player(object):
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

class Tournament(object):
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
		
class Database(object):
    
    k = 15
    
    defaultrating = 1600

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
                        rated = tournament.getAttribute("rated")
                        if not rated or rated == "True":
                            rated = True
                        else:
                            rated = False
                        t = Tournament(games, date, name)
                        t.rated = rated
                        for g in t.games:
                            g.setTournament(t)
                        self.tournaments.append(t)
        f.close()
        self.tournaments = sorted(self.tournaments, key=lambda x:x.year)

    def FindGames(self, p1=None, p2=None):
        return [game for t in self.tournaments for game in t.games if 
                (p2 == None) and (game.red == p1 or game.black == p1) or
                ((game.red == p1 or game.red == p2) and (game.black == p1 or game.black == p2))]

    def PrintPairStats(self, p1, p2):
        games = self.FindGames(p1, p2)
        win = 0
        draw = 0
        lose = 0
        for g in games:
            #print(g)
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
        #print(p1.name, p2.name, win, draw, lose)
        return (p1.name, p2.name, win, draw, lose)

    def PrintStats(self, cutoff):
        tmp = sorted(self.players, key=lambda x: -x.rating)
        tmp = [p for p in tmp if not p.foreign]
        for p1 in tmp[:cutoff]:
            todo = []
            for p2 in tmp[:cutoff]:
                if p1 != p2:
                    res = self.PrintPairStats(p1, p2)
                    todo.append(res)
            st = p1.shortName()
            for t in todo:
                st += "\t+%d =%d -%d" % (t[2], t[3], t[4])
            print(st)
                
    
    def PrintTotalStats(self):
        for p in self.players:
            if not p.foreign:
                win = 0
                lose = 0
                draw = 0
                for g in self.FindGames(p):
                    if g.result == 0.5:
                        draw += 1
                    if g.result == 1:
                        if g.red == p:
                            win += 1
                        else:
                            lose += 1
                    if g.result == 0:
                        if g.black == p:
                            win += 1
                        else:
                            lose += 1
                print("%s\t%d\t+%d =%d -%d " % (p.shortName(), win + draw + lose, win, draw, lose))        
 
    def CorrectRating(self):
        m = 0
        for p in self.players:
            m1 = len(self.FindGames(p))
            if m1 > m:
                m = m1
        for p in self.players:
            m1 = len(self.FindGames(p))
            if m1 < 30:
                p.rating = self.defaultrating + 5 * (p.rating - self.defaultrating) * (m1 / m)
                
    def CorrectRatingPlus(self):
        total = sum([len(t.games) for t in self.tournaments])
        total = total / len(self.players)
        for p in self.players:
            p.rating = self.defaultrating + (p.rating - self.defaultrating) * (min(5, len(self.FindGames(p)) - total) / total)

    def CorrectRatingMinus(self):
        for p in self.players:
            m1 = len(self.FindGames(p))
            if m1 < 25:
                p.rating = p.rating - 50
        
    def ComputeRating(self):
        year = self.tournaments[0].year
        self.ratings = {}
        for p in self.players:
            self.ratings[p] = []
        while True:
            tourn = [x for x in self.tournaments if (x.year == year) and x.rated]
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
                new = p.rating + self.k * dif
                if p.name == "Дмитрий Гладышев":
                    print(year, expScore, realScore, "/", len(currentPlayers[p][1]), p.rating, new, new-p.rating)
                #if not p.foreign:
                #    print(p.name, year, expScore, realScore, "/", len(currentPlayers[p][1]), p.rating, new, new-p.rating)
                newRating[p] = new
            for p in newRating:
                p.rating = newRating[p]
            year += 1
            for p in self.players:
                rat = int(p.rating + 0.5)
                m1 = len([g for g in self.FindGames(p) if g.tournament.year <= year ])
                if m1 < 25:
                    rat = rat - 50
                self.ratings[p].append(rat)
            
    def ComputeRatingTournaments(self):
        self.ratings = {}
        for p in self.players:
            self.ratings[p] = []
        for t in self.tournaments:
            currentPlayers = {}
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
                new = p.rating + self.k * dif
                if p.name == "Даниил Зорин":
                    print(t.name, expScore, realScore, "/", len(currentPlayers[p][1]), p.rating, new, new-p.rating)
                #if not p.foreign:
                #    print(t.name, p.name, expScore, realScore, p.rating, new)
                newRating[p] = new
            for p in newRating:
                p.rating = newRating[p]
            for p in self.players:
                rat = int(p.rating + 0.5)
                m1 = len([g for g in self.FindGames(p)])
                if m1 < 25:
                    rat = rat - 50
                self.ratings[p].append(rat)


db = Database()
db.loadFromXml("tournaments.xml")
'''for t in db.tournaments:
    t.findPlaces()
    for p in t.places:
        if p[1].name == "Даниил Зорин":
            pass
            print(t.name, p[0], p[2])'''
db.ComputeRating()
#db.CorrectRating()
db.CorrectRatingMinus()
tmp = sorted(db.players, key=lambda x: -x.rating)
tmp = [p for p in tmp if not p.foreign]
me = None
mm = 1
pos = 0
for p in tmp:
    print(p.name, int(p.rating + 0.5))
cutoff = 5
print (len([g for t in db.tournaments for g in t.games]))
'''for p in tmp:
    st = p.name[p.name.find(" ") + 1:] + " " + p.name[0]
    for r in db.ratings[p]:
        st += "\t" + str(r)
    print(st)'''
#db.PrintTotalStats()
#db.PrintStats(cutoff)