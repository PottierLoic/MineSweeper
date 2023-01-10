# board class of the minesweeper  
# Author : Loïc Pottier
# Creation date : 21/12/2022

# IMPORTS
import random

# other files from this project
from constants import *

class Board():
    def __init__(self):
        self.board=[]
        self.supBoard=[]
        self.oldBoard=[]
        self.finished=False

        # Creation and filling of the main and real board with 0
        for i in range(HEIGHT):
            self.board.append([])
            self.supBoard.append([])
            self.oldBoard.append([])
            for j in range(WIDTH):
                self.board[i].append(0)
                self.supBoard[i].append(0)
                self.oldBoard[i].append("!")


        # random placement of bombs
        for i in range(MINE_AMOUNT):
            while True:
                rx=random.randint(0, WIDTH-1)
                ry=random.randint(0, HEIGHT-1)
                if self.board[ry][rx]!="x":
                    self.board[ry][rx]="x"
                    break

        # calculation of the numbers around the bombs
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.board[y][x]!="x":
                    # List of pos to check for bombs
                    toCheck=[]
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            toCheck.append([y+dy, x+dx])
                    # check bomb presence in each position around actual pos
                    bombs=0
                    for coords in toCheck:
                        if 0<=coords[0]<HEIGHT and 0<=coords[1]<WIDTH:
                            if self.board[coords[0]][coords[1]]=="x":
                                bombs+=1
                    self.board[y][x]=bombs

    # return True if a bomb is discovered
    def checkLoose(self):
        loose=False
        for i in range(len(self.board)):
            for j in range (len(self.board[i])):
                if self.board[i][j]=="x" and self.supBoard[i][j]==1:
                    loose=True
        return loose

    # return True if all bombs are flagged
    def checkWin(self):
        win=True
        for i in range(len(self.board)):
            for j in range (len(self.board[i])):
                if self.board[i][j]=="x" and self.supBoard[i][j]!=2:
                    win=False
        return win

    # this function is called when a case is discovered
    # if this case is a zero, it will discover the 8 cases around it
    # and if the discovered cases are zeros, it will make a recursive call with the coord of the case concerned
    def discoveryExtend(self, x, y):
        if self.supBoard[y][x]==1 and self.board[y][x]==0:
            toCheck=[]
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if 0<=y+dy<HEIGHT and 0<=x+dx<WIDTH:
                        if self.supBoard[y+dy][x+dx]==0:
                            toCheck.append([y+dy, x+dx])

            for coords in toCheck:
                if 0<=coords[0]<HEIGHT and 0<=coords[1]<WIDTH:
                    self.supBoard[coords[0]][coords[1]]=1

            for coords in toCheck:
                if 0<=coords[0]<HEIGHT and 0<=coords[1]<WIDTH:
                    if self.board[coords[0]][coords[1]]==0:
                        self.discoveryExtend(coords[1], coords[0])

    # reset all the board attributes
    def reset(self):
        self.__init__()

    #return a printable string of the main board, for debug purpose
    def __str__(self) -> str:
        r=""
        for y in range(HEIGHT):
            for x in range(WIDTH):
                r+=str(self.board[y][x])+" "
            r+="\n"
        return r


