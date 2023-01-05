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
MINE_AMOUNT=10
HEIGHT=10
WIDTH=10
SQUARE_SIZE=20
BORDER_SIZE=10
NUMBERS=["img/0.png", "img/1.png", "img/2.png", "img/3.png", "img/4.png", "img/5.png", "img/6.png", "img/7.png", "img/8.png"]


# main board class
# does no contain tkinter parts
class Board():
    def __init__(self):
        self.board=[]
        self.supBoard=[]
        self.finished=False

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
    if not b.finished:
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
    else:
        reset()
    
# called by tk when the right click is used
# it change the case to either flagged if it was unknown
# or to unknown if it was flagged
def button2(e):
    x, y = e.x-BORDER_SIZE, e.y-BORDER_SIZE
    posx=x//SQUARE_SIZE
    posy=y//SQUARE_SIZE
    if not b.finished:
        if b.supBoard[posy][posx]==0:
            b.supBoard[posy][posx]=2
        elif b.supBoard[posy][posx]==2:
            b.supBoard[posy][posx]=0
        graphics()

        if b.checkLoose():
            loose()
        elif b.checkWin():
            win()
    else:
        reset()

# clear the main canvas and recreate all the graphics with the latest values
def graphics():
    canvas.delete("all")
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if b.supBoard[y][x]==1:
                if b.board[y][x]=="x":
                    canvas.create_image(x*SQUARE_SIZE + BORDER_SIZE, y*SQUARE_SIZE+BORDER_SIZE, anchor="nw", image=bombImage, tag="case")
                else:
                    canvas.create_image(x*SQUARE_SIZE + BORDER_SIZE, y*SQUARE_SIZE+BORDER_SIZE, anchor="nw", image=NUMBERSTEST[b.board[y][x]], tag="case")
            elif b.supBoard[y][x]==0:
                canvas.create_image(x*SQUARE_SIZE + BORDER_SIZE, y*SQUARE_SIZE+BORDER_SIZE, anchor="nw", image=hiddenImage, activeimage=overImage, tag="case")
            else:
                canvas.create_image(x*SQUARE_SIZE + BORDER_SIZE, y*SQUARE_SIZE+BORDER_SIZE, anchor="nw", image=flagImage, tag="case")
    

# Destroy every graphics elements and add a loose text in canvas
def loose():
    b.finished=True
    canvas.config(bg=LOOSE_COLOR)
    label.config(text="RATIOOO")

# Destroy every graphics elements and add a win text in canvas
def win():
    b.finished=True
    canvas.config(bg=WIN_COLOR)
    label.config(text="WINNNN")

def reset():
    global b
    b=Board()
    canvas.config(bg=BACKGROUND_COLOR)
    label.config(text="MineSweeper")
    graphics()

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

# Creation of the images, need to put this after the main window declaration
# because of the window.update() call otherwise the images are not loaded correctly
NUMBERSTEST=[ImageTk.PhotoImage(Image.open("img/0.png").resize((SQUARE_SIZE, SQUARE_SIZE))),
             ImageTk.PhotoImage(Image.open("img/1.png").resize((SQUARE_SIZE, SQUARE_SIZE))),
             ImageTk.PhotoImage(Image.open("img/2.png").resize((SQUARE_SIZE, SQUARE_SIZE))),
             ImageTk.PhotoImage(Image.open("img/3.png").resize((SQUARE_SIZE, SQUARE_SIZE))),
             ImageTk.PhotoImage(Image.open("img/4.png").resize((SQUARE_SIZE, SQUARE_SIZE))),
             ImageTk.PhotoImage(Image.open("img/5.png").resize((SQUARE_SIZE, SQUARE_SIZE))),
             ImageTk.PhotoImage(Image.open("img/6.png").resize((SQUARE_SIZE, SQUARE_SIZE))),
             ImageTk.PhotoImage(Image.open("img/7.png").resize((SQUARE_SIZE, SQUARE_SIZE))),
             ImageTk.PhotoImage(Image.open("img/8.png").resize((SQUARE_SIZE, SQUARE_SIZE))),]

overImage=ImageTk.PhotoImage(Image.open("img/over.png").resize((SQUARE_SIZE, SQUARE_SIZE)))
bombImage=ImageTk.PhotoImage(Image.open("img/bomb.png").resize((SQUARE_SIZE, SQUARE_SIZE)))
hiddenImage=ImageTk.PhotoImage(Image.open("img/hidden.png").resize((SQUARE_SIZE, SQUARE_SIZE)))
flagImage=ImageTk.PhotoImage(Image.open("img/flag.png").resize((SQUARE_SIZE, SQUARE_SIZE)))

#affichage du plateau
graphics()

# IA PART

AISPEED=100
aiBoard=[]

def initAIBoard():
    for i in range(HEIGHT):
            aiBoard.append([])
            for j in range(WIDTH):
                aiBoard[i].append(0)

def updateAIBoard():
    for y in range(len(b.board)):
        for x in range (len(b.board[y])):
            if b.supBoard[y][x]==1:
                aiBoard[y][x]=b.board[y][x] 
            elif b.supBoard[y][x]==2:
                aiBoard[y][x]="~"
            else:
                aiBoard[y][x]="*"

def printAIBoard():
    for y in range(len(aiBoard)):
        for x in range (len(aiBoard[y])):
            print(aiBoard[y][x], end="")
        print()

# do the first random click on the board
# then start the ai function
def startAI():
    initAIBoard()
    updateAIBoard()
    x=random.randint(0, WIDTH-1)
    y=random.randint(0, HEIGHT-1)

    canvas.event_generate('<Button-1>', x=x*SQUARE_SIZE+BORDER_SIZE+SQUARE_SIZE/2, y=y*SQUARE_SIZE+BORDER_SIZE+SQUARE_SIZE/2)

    window.after(AISPEED, ai)

# main ai
def ai():  
    updateAIBoard()
    #put all the cases filled with number other than 0 in a list
    caseToCheck=[]
    for y in range(len(aiBoard)):
        for x in range (len(aiBoard[y])):
            if aiBoard[y][x] not in ("*", 0):
                caseToCheck.append((y, x))

    #check around cases in caseToCheck if :
    # first : there is a number of unknown cases around equal to the number of the case - number of flags around already placed
    #   if yes, add the unknown cases to the list of cases to flag
    # second : there is a number of flagged cases around equal to the number of the case
    #   if yes, add the unknown cases remaining around to the list of cases to click
    caseToClick=[]
    caseToFlag=[]
    for case in caseToCheck:
        localToCheck=[]
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                localToCheck.append([case[0]+dy, case[1]+dx])
        unknown=0
        flagged=0
        for coords in localToCheck:
            if 0<=coords[1]<HEIGHT and 0<=coords[0]<WIDTH:
                if aiBoard[coords[0]][coords[1]]=="*":
                    unknown+=1
                elif aiBoard[coords[0]][coords[1]]=="~":
                    flagged+=1
        
    
    print(caseToClick)
    print(caseToFlag)
    for case in caseToClick:
        canvas.event_generate('<Button-1>', x=case[1]*SQUARE_SIZE+BORDER_SIZE+SQUARE_SIZE/2, y=case[0]*SQUARE_SIZE+BORDER_SIZE+SQUARE_SIZE/2)
    for case in caseToFlag:
        canvas.event_generate('<Button-3>', x=case[1]*SQUARE_SIZE+BORDER_SIZE+SQUARE_SIZE/2, y=case[0]*SQUARE_SIZE+BORDER_SIZE+SQUARE_SIZE/2)
    print("dzadazd")
    window.after(AISPEED, ai)

startAI()

window.mainloop()


