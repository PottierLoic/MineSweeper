# MineSweeper   
# Author : Loïc Pottier
# Creation date : 21/12/2022

# IMPORTS
from tkinter import *
from PIL import Image, ImageTk
import random

# CONSTANTS
BACKGROUND_COLOR = "#E0E0E0"
WIN_COLOR = "#00FF00"
LOOSE_COLOR = "#FF0000"
MINE_AMOUNT=20
HEIGHT=15
WIDTH=15
SQUARE_SIZE=20
BORDER_SIZE=10
NUMBERS=["img/0.png", "img/1.png", "img/2.png", "img/3.png", "img/4.png", "img/5.png", "img/6.png", "img/7.png", "img/8.png"]


# main board class
# does no contain tkinter parts
class Board():
    def __init__(self):
        self.board=[]
        self.supBoard=[]

        # Creation and filling of the main and real board with 0
        for i in range(HEIGHT):
            self.board.append([])
            self.supBoard.append([])
            for j in range(WIDTH):
                self.board[i].append(0)
                self.supBoard[i].append(0)


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
                        if 0<=coords[1]<HEIGHT and 0<=coords[0]<WIDTH:
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
                if 0<=coords[1]<HEIGHT and 0<=coords[0]<WIDTH:
                    self.supBoard[coords[0]][coords[1]]=1

            for coords in toCheck:
                if 0<=coords[1]<HEIGHT and 0<=coords[0]<WIDTH:
                    if self.board[coords[0]][coords[1]]==0:
                        self.discoveryExtend(coords[1], coords[0])

    #return a printable string of the main board, for debug purpose
    def __str__(self) -> str:
        r=""
        for y in range(HEIGHT):
            for x in range(WIDTH):
                r+=str(self.board[y][x])+" "
            r+="\n"
        return r

# called by tk when the left click is used
# it change the case to either discovered if it was unknown
# or to unknown if it was flagged
def button1(e):
    x, y = e.x-BORDER_SIZE, e.y-BORDER_SIZE
    posx=x//SQUARE_SIZE
    posy=y//SQUARE_SIZE
    if b.supBoard[posy][posx]==0:
        b.supBoard[posy][posx]=1
    elif b.supBoard[posy][posx]==2:
        b.supBoard[posy][posx]=0
    b.discoveryExtend(posx, posy)
    graphics()

    if b.checkLoose():
        loose()
    elif b.checkWin():
        win()
    
# called by tk when the right click is used
# it change the case to either flagged if it was unknown
# or to unknown if it was flagged
def button2(e):
    x, y = e.x-BORDER_SIZE, e.y-BORDER_SIZE
    posx=x//SQUARE_SIZE
    posy=y//SQUARE_SIZE
    if b.supBoard[posy][posx]==0:
        b.supBoard[posy][posx]=2
    elif b.supBoard[posy][posx]==2:
        b.supBoard[posy][posx]=0
    graphics()

    if b.checkLoose():
        loose()
    elif b.checkWin():
        win()

# clear the main canvas and recreate all the graphics with the latest values
def graphics():
    canvas.delete("all")
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if b.supBoard[y][x]==1:
                if b.board[y][x]=="x":
                    imgList.append(ImageTk.PhotoImage(Image.open("img/bomb.png").resize((SQUARE_SIZE, SQUARE_SIZE))))
                    canvas.create_image(x*SQUARE_SIZE + BORDER_SIZE, y*SQUARE_SIZE+BORDER_SIZE, anchor="nw", image=imgList[-1], tag="case")
                else:
                    imgList.append(ImageTk.PhotoImage(Image.open(NUMBERS[b.board[y][x]]).resize((SQUARE_SIZE, SQUARE_SIZE))))
                    canvas.create_image(x*SQUARE_SIZE + BORDER_SIZE, y*SQUARE_SIZE+BORDER_SIZE, anchor="nw", image=imgList[-1], tag="case")
            elif b.supBoard[y][x]==0:
                imgList.append(ImageTk.PhotoImage(Image.open("img/hidden.png").resize((SQUARE_SIZE, SQUARE_SIZE))))
                canvas.create_image(x*SQUARE_SIZE + BORDER_SIZE, y*SQUARE_SIZE+BORDER_SIZE, anchor="nw", image=imgList[-1], activeimage=overImage, tag="case")
            else:
                imgList.append(ImageTk.PhotoImage(Image.open("img/flag.png").resize((SQUARE_SIZE, SQUARE_SIZE))))
                canvas.create_image(x*SQUARE_SIZE + BORDER_SIZE, y*SQUARE_SIZE+BORDER_SIZE, anchor="nw", image=imgList[-1], tag="case")

# Destroy every graphics elements and add a loose text in canvas
def loose():
    canvas.config(bg=LOOSE_COLOR)
    label.config(text="RATIOOO")

# Destroy every graphics elements and add a win text in canvas
def win():
    canvas.config(bg=WIN_COLOR)
    label.config(text="WINNNN")

window = Tk()
window.title("MineSweeper")
window.resizable(False, False)

label = Label(window, text="MineSweeper", font=("consolas", 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=HEIGHT*SQUARE_SIZE+BORDER_SIZE*2, width=WIDTH*SQUARE_SIZE+BORDER_SIZE*2)
canvas.pack()

window.update()

windowWidth = window.winfo_width()
windowHeight = window.winfo_height()
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()

x = int((screenWidth/2) - (windowWidth/2))
y = int((screenHeight/2) - (windowHeight/2))

window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")

b = Board()


# keybinds
window.bind('<Button-1>', button1)
window.bind('<Button-3>', button2)

#affichage du plateau
overImage=ImageTk.PhotoImage(Image.open("img/over.png").resize((SQUARE_SIZE, SQUARE_SIZE)))
imgList=[]
canvas.delete("all")

graphics()
    
window.mainloop()


