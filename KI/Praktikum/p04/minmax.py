from abc import ABC, abstractmethod
from tkinter import *

import copy

import threading

import time

class Action:
    def __init__(self, x, y, sign):
        self.x = x
        self.y = y
        self.sign = sign

    def __str__(self):
        return ("Action:{x: %d, y: %d, sign: %s}" % (self.x, self.y, self.sign))

class Board:
    def __init__(self, b = None):
        if b is None:
            self.b = [[0 for x in range(3)] for y in range(3)]
            for x in range(0,3):
                for y in range(0,3):
                    self.b[x][y] = " "
        else:
            self.b = copy.deepcopy(b)

    def set(self, action):
        self.b[action.x][action.y] = action.sign

    def getCell(self, x, y):
        return self.b[x][y]

    def count(self, sign):
        _count = 0
        for x in range(0, 3):
            for y in range(0, 3):
                if self.b[x][y] == sign:
                    _count += 1
        return _count

    def getSuccessors(self):
        successors = []
        for x in range(0, 3):
            for y in range(0, 3):
                if self.b[x][y] == " ":
                    successor = Board(self.b)
                    if self.count("x") > self.count("o"):
                        action = Action(x, y, "o")
                    else:
                        action = Action(x, y, "x")
                    successor.set(action)
                    successors.append((successor, action))
        return successors

    def utility(self, sign):
        validSigns = ["x", "o"]
        if sign not in validSigns:
            raise ValueError("sign not valid")
        if sign is validSigns[0]:
            minSign = validSigns[1]
        else:
            minSign = validSigns[0]

        for i in range(0, 3):
            if self.b[i][0] == minSign and self.b[i][1] == minSign and self.b[i][2] == minSign:
                return -1
            if self.b[i][0] == sign and self.b[i][1] == sign and self.b[i][2] == sign:
                return 1
            if self.b[0][i] == minSign and self.b[1][i] == minSign and self.b[2][i] == minSign:
                return -1
            if self.b[0][i] == sign and self.b[1][i] == sign and self.b[2][i] == sign:
                return 1

        if self.b[0][0] == minSign and self.b[1][1] == minSign and self.b[2][2] == minSign:
            return -1
        if self.b[2][0] == minSign and self.b[1][1] == minSign and self.b[0][2] == minSign:
            return -1


        if self.b[0][0] == sign and self.b[1][1] == sign and self.b[2][2] == sign:
            return 1
        if self.b[2][0] == sign and self.b[1][1] == sign and self.b[0][2] == sign:
            return 1

        return 0

    def terminalTest(self):
        if self.utility("x") != 0 or len(self.getSuccessors()) == 0:
            return True
        return False

    def whoWon(self):
        u = self.utility("x")
        if u == 1:
            return "player X won"
        elif u == -1:
            return "player O won"
        else:
            return "tie. everyone loses!"


    def __str__(self):
        _str = "Board:\n"
        for y in range(0, 3):
            for x in range(0, 3):
                _str += self.b[x][y]
                if x < 2: _str += " "
            _str += "\n"
        return _str


class Strategy(ABC):
    @abstractmethod
    def apply(self, board):
        pass

class MinMax(Strategy):

    def __init__(self, sign):
        self.sign = sign

    def apply(self, board):
        self.nodeCount = 0

        (val, action) = (float("-INF"), None)
        for (b, a) in board.getSuccessors():
            v = self.MinValue(b)
            if (val <= v):
                (val, action) = (v, a)
        print("Knotenanzahl: ", self.nodeCount)
        return action

    def MaxValue(self, board):
        self.nodeCount += 1
        if board.terminalTest(): return board.utility(self.sign)

        v = float("-INF")
        for (b, a) in board.getSuccessors():
            v = max(v, self.MinValue(b))
        return v

    def MinValue(self, board):
        self.nodeCount += 1
        if board.terminalTest(): return board.utility(self.sign)

        v = float("INF")
        for (b, a) in board.getSuccessors():
            v = min(v, self.MaxValue(b))
        return v

class MinMax2(MinMax):
    def __init__(self, sign):
        super().__init__(sign)

    def MaxValue(self, board, alpha=float("-INF"), beta=float("INF")):
        self.nodeCount += 1
        if board.terminalTest(): return board.utility(self.sign)

        v = float("-INF")
        for (b, a) in board.getSuccessors():
            v = max(v, self.MinValue(b, alpha, beta))
            if v >= beta: return v
            alpha = max(alpha, v)
        return v

    def MinValue(self, board, alpha=float("-INF"), beta=float("INF")):
        self.nodeCount += 1
        if board.terminalTest(): return board.utility(self.sign)

        v = float("INF")
        for (b, a) in board.getSuccessors():
            v = min(v, self.MaxValue(b, alpha, beta))
            if v <= alpha: return v
            beta = min(beta, v)
        return v

class Player(Strategy):
    def __init__(self, canvas):
        canvas.bind("<ButtonPress-1>", self.callback)
        self.action = None

    def callback(self, event):
        for x in range(0, 3):
            for y in range(0, 3):
                if(event.x in range(x*100, (x+1)*100) and event.y in range(y*100, (y+1)*100)):
                    self.action = Action(x, y, "x")

    def isValid(self, board, action):
        if action is not None and board.getCell(action.x, action.y) is " ": return True
        return False

    def apply(self, board):
        a = self.action
        self.action = None
        if self.isValid(board, a): return a
        return None




class Main:
    def applyAction(self, action):
        self.board.set(action)
        if action.sign == "x":
            self.cross(action.x, action.y)
        elif action.sign == "o":
            self.circle(action.x, action.y)
            self.myTurn = True

    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.pack(fill="both", expand=True)
        self.canvas = Canvas(self.frame, width=300, height=300)
        # self.canvas.bind("<ButtonPress-1>", self.callback)
        self.canvas.pack(fill="both", expand=True)

        self.label=Label(self.frame, text='Tic Tac Toe Game', height=3, bg='black', fg='blue')
        self.label.pack(fill="both", expand=True)

        self._board()


        self.myTurn = True
        self.player1 = Player(self.canvas)
        self.player2 = MinMax2("o")
        self.board = Board()



    def _board(self):
        self.canvas.create_rectangle(0,0,300,300, outline="black")
        self.canvas.create_rectangle(100,300,200,0, outline="black")
        self.canvas.create_rectangle(0,100,300,200, outline="black")

    def cross(self, x, y):
        xCoord = (200*x+100)/2
        yCoord = (200*y+100)/2
        self.canvas.create_line( xCoord+20, yCoord+20, xCoord-20, yCoord-20, width=4, fill="black")
        self.canvas.create_line( xCoord-20, yCoord+20, xCoord+20, yCoord-20, width=4, fill="black")

    def circle(self, x, y):
        xCoord = (200*x+100)/2
        yCoord = (200*y+100)/2

        self.canvas.create_oval( xCoord+25, yCoord+25, xCoord-25, yCoord-25, width=4, outline="black")


def myLoop():
    global player, app, root

    if app.board.terminalTest():
        print(app.board.whoWon())
        time.sleep(1)
        root.quit()
        return
    action = player.apply(app.board)
    if action is not None:
        app.applyAction(action)
        if player is app.player1:
            player = app.player2
        else:
            player = app.player1
    root.after(10, myLoop)


root=Tk()
app = Main(root)
player = app.player1
root.after(10, myLoop)
root.mainloop()
