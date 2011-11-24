import re, copy

class Piece:
    Empty = 0
    King = 1
    Advisor = 2
    Elephant = 3
    Horse = 4
    Rook = 5
    Cannon = 6
    Pawn = 7
    
    @staticmethod
    def fromString(s):
        if s == 'R':
            return Piece.Rook
        elif s == 'H':
            return Piece.Horse
        elif s == 'E':
            return Piece.Elephant
        elif s == 'A':
            return Piece.Advisor
        elif s == 'G':
            return Piece.King
        elif s == 'C':
            return Piece.Cannon
        elif s == 'S':
            return Piece.Pawn
    @staticmethod
    def toString(s):
        if s == Piece.Rook:
            return 'R'
        elif s == Piece.Horse:
            return 'H'
        elif s == Piece.Elephant:
            return 'E'
        elif s == Piece.Advisor:
            return 'A'
        elif s == Piece.King:
            return 'G'
        elif s == Piece.Cannon:
            return 'C'
        elif s == Piece.Pawn:
            return 'S'
        else:
            return " "
    
class Color:
    Red = 1
    Black = -1
    
    @staticmethod
    def toString(c):
        if c == 1:
            return 'r'
        else:
            return 'b'

class WrongMove(Exception):
    def __init__(self, m):
        self.msg = m
    def __str__(self):
        return self.msg
        
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y   
    def __str__(self):
        return str(chr(self.x + ord('a') - 1)) + str(self.y)
    def isEqual(self, pos):
        return self.x == pos.x and self.y == pos.y
    def sameRow(self, pos):
        return self.y == pos.y
    def sameColumn(self, pos):
        return self.x == pos.x
    def sameDiagonal(self, pos):
        return abs(self.y - pos.y) == abs(self.x - pos.x)
    def inCastle(self, color):
        if self.x <= 6 and self.x >= 4:
            if (color == Color.Red and self.y <= 3) or (color == Color.Black and self.y >= 8):
                return True
        return False
    def onSide(self, color):
        if (color == Color.Red and self.y <= 5) or (color == Color.Black and self.y >= 6):
            return True
        return False
    def distance(self, pos):
        return max(abs(self.x - pos.x), abs(self.y - pos.y))
    def getElephantBlock(self, dst):
        y = (self.y + dst.y) / 2
        x = (self.x + dst.x) / 2
        return Position(x, y)
    def horseMove(self, dst):
        if self.distance(dst) == 2:
            if abs(self.x - dst.x) == 1 or abs(self.y - dst.y) == 1:
                return True
        return False
    def getHorseBlock(self, dst):
        if abs(self.y - dst.y) == 1:
            if self.x > dst.x:
                return Position(self.x - 1, self.y)
            else:
                return Position(self.x + 1, self.y)
        elif abs(self.x - dst.x) == 1:
            if self.y > dst.y:
                return Position(self.x, self.y - 1)
            else:
                return Position(self.x, self.y + 1)
        
class Board:
    def __init__(self):
        self.board = [
                      [5, 4, 3, 2, 1, 2, 3, 4, 5],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 6, 0, 0, 0, 0, 0, 6, 0],
                      [7, 0, 7, 0, 7, 0, 7, 0, 7],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [-7, 0, -7, 0, -7, 0, -7, 0, -7],
                      [0, -6, 0, 0, 0, 0, 0, -6, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [-5, -4, -3, -2, -1, -2, -3, -4, -5]]
        self.pieces = {}
        for i in range(10):
            for j in range(9):
                p = self.board[i][j]
                if p != Piece.Empty:
                    self.pieces[(i, j)] = p
        '''self.board = [
                      [0, 0, 0, 0, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 6, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 7, 0, 7, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, -7, 0, -7, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, -6, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, -1, 0, 0, 0, 0]]'''

    def __str__(self):
        res = ""
        for row in self.board[::-1]:
            for column in row:
                if column == 0:
                    res += "  "
                else:
                    res += Color.toString(column/abs(column)) + Piece.toString(abs(column))
            res += "\n"
        return res
    def equals(self, other):
        for i in range(10):
            for j in range(9):
                if other.board[i][j] != self.board[i][j]:
                    return False
        return True        
    def getPiece(self, pos):
        return self.board[pos.y-1][pos.x-1]

    def piecesBetween(self, src, dst):
        counter = 0
        if src.x == dst.x:
            for i in range(min(src.y, dst.y) + 1, max(src.y, dst.y)):
                if self.getPiece(Position(src.x, i)) != Piece.Empty:
                    counter += 1
        if src.y == dst.y:
            for i in range(min(src.x, dst.x) + 1, max(src.x, dst.x)):
                if self.getPiece(Position(i, src.y)) != Piece.Empty:
                    counter += 1
        return counter
    
    def tryMovePiece(self, color, src, dst):
        piece = self.getPiece(src)
        if piece * color < 0:
            raise WrongMove("Wrong color")
        
        if piece == 0:
            raise WrongMove("No piece")
        
        if self.getPiece(dst) * color > 0:
            raise WrongMove("Trying to capture own piece")
        
        piecet = abs(piece)
        if piecet == Piece.King:
            if not (src.sameRow(dst) or src.sameColumn(dst)) or src.distance(dst) > 1:
                raise WrongMove("King movement direction is incorrect")
            if not dst.inCastle(color):
                raise WrongMove("King moves out of castle")
        if piecet == Piece.Advisor:
            if not src.sameDiagonal(dst) or src.distance(dst) > 1:
                raise WrongMove("Advisor movement direction is incorrect")
            if not dst.inCastle(color):
                raise WrongMove("Advisor moves out of castle")
        if piecet == Piece.Elephant:
            if not src.sameDiagonal(dst) or src.distance(dst) != 2:
                raise WrongMove("Elephant movement direction is incorrect")
            if not dst.onSide(color):
                raise WrongMove("Elephant moves out of castle")
            if self.getPiece(src.getElephantBlock(dst)) != 0:
                raise WrongMove("Elephant is blocked")
        if piecet == Piece.Horse:
            if not src.horseMove(dst):
                raise WrongMove("Horse movement direction is incorrect")
            if self.getPiece(src.getHorseBlock(dst)) != 0:
                raise WrongMove("Horse is blocked")
        if piecet == Piece.Rook:
            if not (src.sameRow(dst) or src.sameColumn(dst)):
                raise WrongMove("Rook movement direction is incorrect")
            if self.piecesBetween(src, dst) > 0:
                raise WrongMove("Rook skipping over pieces")
        if piecet == Piece.Cannon:
            if not (src.sameRow(dst) or src.sameColumn(dst)):
                raise WrongMove("Rook movement direction is incorrect")
            if self.getPiece(dst) != Piece.Empty:
                if self.piecesBetween(src, dst) != 1:
                    raise WrongMove("Cannon can't kill without skipping over a piece")
            else:
                if self.piecesBetween(src, dst) > 0:
                    raise WrongMove("Cannon can't move skipping over pieces")
        if piecet == Piece.Pawn:
            if not (src.sameRow(dst) or src.sameColumn(dst)) or src.distance(dst) > 1:
                raise WrongMove("Pawn movement direction is incorrect")
            if (color == Color.Red and dst.y < src.y) or (color == Color.Black and dst.y > src.y):
                raise WrongMove("Pawn can't move backwards")
            if src.y == dst.y and src.onSide(color):
                raise WrongMove("Pawn can't move sideways yet")
        
        return True
    
    def movePiece(self, src, dst):
        p = self.getPiece(src)
        self.board[dst.y-1][dst.x-1] = p
        self.board[src.y-1][src.x-1] = Piece.Empty
        del self.pieces[(src.y-1, src.x-1)]
        pos = (dst.y-1, dst.x-1)
        self.pieces[pos] = p
        
    def printMove(self, move):
        print(Piece.toString(abs(self.getPiece(move.src))) + str(move.src) + "-" + str(move.dst))

    def getPositions(self, pos, piece):
        def addPos(i, j):
            if i >= 1 and i <= 9 and j >= 1 and j <= 10:
                res.append(Position(i, j))
        s = piece
        res = []
        if (s == Piece.Rook) or (s == Piece.Cannon):
            for i in range(10):
                addPos(pos.x, i + 1)
            for i in range(9):
                addPos(i + 1, pos.y)
        elif s == Piece.Horse:
            addPos(pos.x + 1, pos.y + 2)
            addPos(pos.x + 1, pos.y - 2)
            addPos(pos.x - 1, pos.y + 2)
            addPos(pos.x - 1, pos.y - 2)
            addPos(pos.x + 2, pos.y + 1)
            addPos(pos.x + 2, pos.y - 1)
            addPos(pos.x - 2, pos.y + 1)
            addPos(pos.x - 2, pos.y - 1)
        elif s == Piece.Elephant:
            addPos(pos.x + 2, pos.y + 2)
            addPos(pos.x + 2, pos.y - 2)
            addPos(pos.x - 2, pos.y + 2)
            addPos(pos.x - 2, pos.y - 2)
        elif s == Piece.Advisor:
            addPos(pos.x + 1, pos.y + 1)
            addPos(pos.x + 1, pos.y - 1)
            addPos(pos.x - 1, pos.y + 1)
            addPos(pos.x - 1, pos.y - 1)
        elif s == Piece.King:
            addPos(pos.x + 1, pos.y)
            addPos(pos.x, pos.y + 1)
            addPos(pos.x - 1, pos.y)
            addPos(pos.x, pos.y - 1)
        elif s == Piece.Pawn:
            addPos(pos.x + 1, pos.y)
            addPos(pos.x, pos.y + 1)
            addPos(pos.x - 1, pos.y)
            addPos(pos.x, pos.y - 1)   
        return res    
    def getAllMoves(self, color):
        res = []
        for k in self.pieces.keys():
            piece = self.pieces[k]
            src = Position(k[1] + 1, k[0] + 1)
            apiece = abs(piece)
            for pos in self.getPositions(src, apiece):
                try:
                    dst = pos
                    col = piece/apiece
                    if col == color:
                        #print("trying ", src, dst)
                        self.tryMovePiece(col, src, dst)
                        res.append(Move(col, src, dst))
                except:
                    pass
        return res

    def _getNewBoard(self, src, dst):
        newb = Board()
        for i in range(10):
            for j in range(9):
                newb.board[i][j] = self.board[i][j]
        for k in self.pieces.keys():
            newb.pieces[k] = self.pieces[k]
        newb.movePiece(src, dst)
        return newb
    
    def isCheck(self, color):
        kingpos = None
        otherkingpos = None
        for i in range(10):
            for j in range(9):
                if self.board[i][j] == Piece.King * -color:
                    kingpos = Position(j + 1, i + 1)
                elif self.board[i][j] == Piece.King * color:
                    otherkingpos = Position(j + 1, i + 1)
        for m in self.getAllMoves(color):
            if self.getPiece(m.src) * color > 0 and m.dst.isEqual(kingpos):
                return True
        if kingpos.sameColumn(otherkingpos) and self.piecesBetween(kingpos, otherkingpos) == 0:
            return True
        return False 
    
    def isCheckmate(self, color):
        if self.isCheck(color):
            for m in self.getAllMoves(-color):
                newb = self._getNewBoard(m.src, m.dst)
                if not newb.isCheck(color):
                    print("Protect with ", m)
                    return False
            return True
        else:
            return False
        
class Move:
    def __init__(self, color, src, dst):
        self.color = color
        self.src = src
        self.dst = dst
    def __str__(self):
        return str(self.src) + str(self.dst)

class XiangqiGame:
    def __init__(self):
        self.moves = []
        self.positions = []
    def addMove(self, m):  
        self.moves.append(m)
    def addPosition(self, p):
        self.positions.append(copy.deepcopy(p))
    def checkRepetition(self):
        lastp = self.positions[-1]
        counter = 0
        for p in self.positions[:len(self.positions)-2]:
            if lastp.equals(p):
                counter += 1
        if counter == 4:
            return True
        return False
    def getMove(self, color):
        s = input("Move " + ("Red" if color == 1 else "Black") + " >")
        europe = re.compile('(R|H|E|A|G|C|S)([a-i])(10|[1-9])-([a-i])(10|[1-9])')
        china = re.compile('(R|H|E|A|G|C|S)([1-9]|\^|v)(\+|-|=)([1-9])')
        ma = europe.match(s)
        if not ma:
            raise WrongMove("Wrong format")
        piece = Piece.fromString(ma.group(1))
        m = Move(color,
                 Position(ord(ma.group(2)) - ord('a') + 1, int(ma.group(3))), 
                 Position(ord(ma.group(4)) - ord('a') + 1, int(ma.group(5))))
        return piece, m
    
class AI:
    Depth = 3
    strength = {Piece.King:9000, Piece.Advisor: 2, Piece.Elephant:3, 
                Piece.Horse:4.5, Piece.Cannon:5, Piece.Rook:9}
    def __init__(self, pos, color):
        self.position = pos
        self.color = color

    def thinkMove(self, color):
        tree = SearchTree(self.position, color, None)
        tree.build(self.Depth)
        tree.minimax(color)
        #tree.printMoves()
        #tree.printPaths()
        return tree.selectMax(color)
        
    @staticmethod
    def evaluate(pos):
        val = 0
        for i in range(10):
            for j in range(9):
                piece = pos.board[i][j]
                if piece != Piece.Empty:
                    apiece = abs(piece)
                    color = piece / apiece
                    if apiece != Piece.Pawn:
                        val += AI.strength[apiece] * color
                    else:
                        p = Position(j + 1, i + 1)
                        if p.onSide(color):
                            val += 1 * color
                        else:
                            val += 2.5 * color
        return val

class SearchTree:                
    def __init__(self, pos, color, move):
        self.children = []
        self.position = pos
        self.color = color
        self.move = move
        self.value = 0
    def printTree(self):
        print(self.position)
        for c in self.children:
            c.printTree()
    def printMoves(self):
        for c in self.children:
            print (c.move, c.value)
    def printPaths(self, parent = ""):
        res = parent
        if self.move != None:
            res += str(self.move) + " "
        print(res, self.value)
        for c in self.children:
            c.printPaths(res)
    def build(self, depth):
        moves = self.position.getAllMoves(self.color)
        for m in moves:
            newb = self.position._getNewBoard(m.src, m.dst)
            self.children.append(SearchTree(newb, -self.color, m))
        if depth > 1:
            i = 0
            for t in self.children:
                i += 1
                t.build(depth - 1)
                if depth > 2:
                    print(depth, i, len(self.children))
    def minimax(self, color):
        if len(self.children) == 0:
            self.value = AI.evaluate(self.position)
            #print(self.move, self.value)
            return
        for c in self.children:
            c.minimax(color)
        vals = [c.value * color for c in self.children]
        if self.color == color:
            self.value = max(vals) * color
            #print("max", self.value, vals)
        else:
            self.value = min(vals) * color
            #print("min", self.value, vals)
    def selectMax(self, color):
        v = self.children[0].value * color
        move = self.children[0].move
        for c in self.children[1:]:
            if c.value * color > v:
                move = c.move
        return move

b = Board()
g = XiangqiGame()
g.addPosition(b)
color = Color.Red
players = {Color.Red:"Human", Color.Black:"Computer"}
comp = AI(b, 1)
move = comp.thinkMove(1)
print(move)
exit(0)
while True:
    try:
        if players[color] == "Human":
            piece, move = g.getMove(color)
            if abs(b.getPiece(move.src)) != piece:
                raise WrongMove("There is no such piece in this position")
            b.tryMovePiece(color, move.src, move.dst)
            newb = b._getNewBoard(move.src, move.dst)
            if newb.isCheck(-color):
                raise WrongMove("You must protect from check")
        elif players[color] == "Computer":
            comp = AI(b, color)
            move = comp.thinkMove(color)
        b.movePiece(move.src, move.dst)
        g.addMove(move)
        g.addPosition(b)
        if b.isCheck(color):
            print("Check!")
        if g.checkRepetition():
            if b.isCheck(color):
                print("Perpetual check")
                break
            else:
                print("Repetition: draw")
                break
        if b.isCheckmate(color):
            print("Checkmate!")
            break
        color = -color
        print(b)
    except WrongMove as e:
        print(e)
    