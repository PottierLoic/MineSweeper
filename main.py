# MineSweeper   
# Author : Loïc Pottier
# Creation date : 21/12/2022

# IMPORTS
from tkinter import *
from PIL import Image, ImageTk
import random
import pattern #pattern.py file of this projets, used to store all patterns and their unique solution

# CONSTANTS
BACKGROUND_COLOR = "#E0E0E0"
WIN_COLOR = "#00FF00"
LOOSE_COLOR = "#FF0000"
MINE_AMOUNT=70
HEIGHT=20
WIDTH=20
SQUARE_SIZE=30
BORDER_SIZE=10

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
def leftClick(e):
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
def rightClick(e):
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

# count the number of mine that we found (number of flags placed) 
# and sbstract them to the MINE_AMOUNT constant, then update the number display
def updateMineNumber():
    nb=0
    for row in b.supBoard:
        for col in row:
            if col==2:
                nb+=1
    minesText="Remaining bombs : "+str(MINE_AMOUNT-nb)
    minesLabel.config(text=minesText)

# clear the main canvas and recreate all the graphics with the actual values
def graphics():
    canvas.delete("all")
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if b.supBoard[y][x]==1:
                if b.board[y][x]=="x":
                    canvas.create_image(x*SQUARE_SIZE + BORDER_SIZE, y*SQUARE_SIZE+BORDER_SIZE, anchor="nw", image=bombImage, tag="case")
                else:
                    canvas.create_image(x*SQUARE_SIZE + BORDER_SIZE, y*SQUARE_SIZE+BORDER_SIZE, anchor="nw", image=NUMBERS[b.board[y][x]], tag="case")
            elif b.supBoard[y][x]==0:
                canvas.create_image(x*SQUARE_SIZE + BORDER_SIZE, y*SQUARE_SIZE+BORDER_SIZE, anchor="nw", image=hiddenImage, activeimage=overImage, tag="case")
            else:
                canvas.create_image(x*SQUARE_SIZE + BORDER_SIZE, y*SQUARE_SIZE+BORDER_SIZE, anchor="nw", image=flagImage, tag="case")
    updateMineNumber()

# Destroy every graphics elements and add a loose text in canvas
def loose():
    global defeat, defeatText
    b.finished=True
    canvas.config(bg=LOOSE_COLOR)
    label.config(text="RATIOOO")
    defeat +=1
    defeatText="Defeat : "+str(defeat)
    defeatLabel.config(text=defeatText)

# Destroy every graphics elements and add a win text in canvas
def win():
    global victory, victoryText
    b.finished=True
    canvas.config(bg=WIN_COLOR)
    label.config(text="WINNNN")
    victory +=1
    victoryText="Victory : "+str(victory)
    victoryLabel.config(text=victoryText)

# reset the board by recreating a new Board object 
# and reverse the changes made by the win/loose function 
def reset():
    global b
    b=Board()
    canvas.config(bg=BACKGROUND_COLOR)
    label.config(text="MineSweeper")
    graphics()

# function used for the first click on the board, as in the original game, we can't loose on the first click
# this function looks for all the 0 in the board, select one randomly and click on it so we don't die 
def discoverFirstCase():
    zeroCase=[]
    for row in range(HEIGHT):
        for col in range(WIDTH):
            if b.board[row][col]==0:
                zeroCase.append([row, col])
    if len(zeroCase)!=0:
        rd=random.choice(zeroCase)
        canvas.event_generate('<Button-1>', x=rd[1]*SQUARE_SIZE+BORDER_SIZE+SQUARE_SIZE/2, y=rd[0]*SQUARE_SIZE+BORDER_SIZE+SQUARE_SIZE/2)
    else:
        unknownList=[]
        for row in range(HEIGHT-1):
            for col in range(WIDTH-1):
                if aiBoard[row][col]=="*":
                    unknownList.append([row, col])
        rd=random.choice(unknownList)
        canvas.event_generate('<Button-1>', x=rd[1]*SQUARE_SIZE+BORDER_SIZE+SQUARE_SIZE/2, y=rd[0]*SQUARE_SIZE+BORDER_SIZE+SQUARE_SIZE/2)

# WINDOW AND TKINTER SECTION
window = Tk()
window.title("MineSweeper")
window.resizable(False, False)

label = Label(window, text="MineSweeper", font=("consolas", 40))
label.pack()

victory=0
defeat=0

victoryText="Victory : "+str(victory)
victoryLabel = Label(window, text=victoryText, font=("consolas", 10))
victoryLabel.pack()

defeatText="Defeats : "+str(defeat)
defeatLabel = Label(window, text=defeatText, font=("consolas", 10))
defeatLabel.pack()

remainingMines=MINE_AMOUNT
minesText="Remaining bombs : "+str(remainingMines)
minesLabel = Label(window, text=minesText, font=("consolas", 10))
minesLabel.pack()

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

# KEYBINDS (if you want to play without ai)
window.bind('<Button-1>', leftClick)
window.bind('<Button-3>', rightClick)

# Creation of the images, need to put this after the main window declaration
# because of the window.update() call otherwise the images are not loaded correctly
NUMBERS=[ImageTk.PhotoImage(Image.open("img/0.png").resize((SQUARE_SIZE, SQUARE_SIZE))),
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

#------------------------------------------------------------------------
# IA PART
#------------------------------------------------------------------------

# set this to false to desactivate AI part and play yourself
AI_ON = True

# Minimum possible value looks to be 4, maybe 1 on a good pc
# the lower the speed is, the faster the ia is, it represent the time waited between every action, so the tkinter interface can follow
AISPEED=1

# creating the board that the ai will analyze
aiBoard=[]

# fill the aiBoard with 0
# so we can update it when in the next function
def initAIBoard():
    global aiBoard
    aiBoard=[]
    for i in range(HEIGHT):
        aiBoard.append([])
        for j in range(WIDTH):
            aiBoard[i].append(0)

# update the ai board using the sup and main board
# in simple terms, it only contain what a real player can see from the game
# every case that is not discovered on the suppBoard will contain "*"
def updateAIBoard():
    for y in range(len(b.board)):
        for x in range (len(b.board[y])):
            if b.supBoard[y][x]==1:
                aiBoard[y][x]=b.board[y][x] 
            elif b.supBoard[y][x]==2:
                aiBoard[y][x]="~"
            else:
                aiBoard[y][x]="*"

# print the aiBoard in cli, used for debug, i leave it here
def printAIBoard():
    for row in aiBoard:
        for col in row:
            print(col, end="")
        print("")
    print("")

# do the first random click on the board
# then start the ai function
# this click can only be done on an empty case
# see the discoverFirstCase function comment for more info
def startAI():
    if AI_ON:
        initAIBoard()
        updateAIBoard()
        discoverFirstCase()

        window.after(AISPEED, ai)

# empty function that we call in the window.after line
# it does nothing but apparently we need a function to be able to wait
def wait():
    pass

# right click on the case specified in parameters --> put a flag
def flagCase(posx, posy):
    canvas.event_generate('<Button-3>', x=posx*SQUARE_SIZE+BORDER_SIZE+SQUARE_SIZE/2, y=posy*SQUARE_SIZE+BORDER_SIZE+SQUARE_SIZE/2)

# left click on the case specified in parameters --> discover the case
def clickCase(posx, posy):
    canvas.event_generate('<Button-1>', x=posx*SQUARE_SIZE+BORDER_SIZE+SQUARE_SIZE/2, y=posy*SQUARE_SIZE+BORDER_SIZE+SQUARE_SIZE/2)

# main ai
def ai():
    updateAIBoard()
    lastAction=[]

    # FIRST PART OF THE AI
    # this part will try to solve the actual state by checking one case at a time
    # it will no take into account the others numbers around it

    #put all the cases filled with number other than 0 in a list
    caseToCheck=[]
    for y in range(len(aiBoard)):
        for x in range (len(aiBoard[y])):
            if aiBoard[y][x] not in ("*", 0, "~", "*"):
                valid=False
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if 0<=y+dy<HEIGHT and 0<=x+dx<WIDTH:
                            if aiBoard[y+dy][x+dx]=="*":
                                valid=True
                if valid:
                    caseToCheck.append((y, x))

    # if the first click is on a number, we need to click on another random case
    # to avoid a random click when we only have one unknown case left, we need to count unknown cases
    totalUnknown=0
    for row in aiBoard:
        for col in row:
            if col=="*":
                totalUnknown+=1

    #check around cases in caseToCheck if :
    # first : there is a number of unknown cases around equal to the number of the case - number of flags around already placed
    #   if yes, call the flagCase function for theses coords
    # second : there is a number of flagged cases around equal to the number of the case
    #   if yes, call the clickCase function for theses coords
    done=False
    for case in caseToCheck:
        if not done:  
            localToCheck=[]

            # For each case, we need to get the coords of all the cases around
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    localToCheck.append([case[0]+dy, case[1]+dx])
            unknown=0
            unknownList=[]
            flagged=0
            # we get the number of flagged and unknown cases in the precedent list
            for coords in localToCheck:
                if 0<=coords[1]<HEIGHT and 0<=coords[0]<WIDTH:
                    if aiBoard[coords[0]][coords[1]]=="*":
                        unknown+=1
                        unknownList.append([coords[0], coords[1]])
                    elif aiBoard[coords[0]][coords[1]]=="~":
                        flagged+=1

            # if the number of unknown cases around is equal to the number on the actual case - flags around
            # we can juste flag every unknown case because there is 0% chance for them to be a bomb
            if type(aiBoard[case[0]][case[1]])==int:
                if unknown==aiBoard[case[0]][case[1]]-flagged:
                    for unknownCase in unknownList:
                        if b.finished:
                            break
                        flagCase(unknownCase[1], unknownCase[0])
                    done=True
            # if the number of flagged cases around is equal to the number on the actual case
            # it means that all the bombs are found, so we can click on every unknown case
            if flagged==aiBoard[case[0]][case[1]]:
                for unknownCase in unknownList:
                    if b.finished:
                        break
                    clickCase(unknownCase[1], unknownCase[0])
                done=True

            #if ai fail, no need to continue
            if b.finished:
                break

    # SECOND PART OF THE AI
    # if the first part does not provide any single action to do, this part is the only way to continue the game
    # it will try to find patterns in the board that allow us to continue by taking into account groups of cases
    if not done:
        patternRecognition=pattern.patternFinder(aiBoard)
        if patternRecognition!=None:
            if patternRecognition[0]=="safe":
                for coords in patternRecognition[1]:
                    clickCase(coords[1], coords[0])
                    lastAction="pattern : clicked on : "+str(coords[1])+", "+str(coords[0])
                    if b.finished:
                        print("raté a cause du pattern")
            else:
                for coords in patternRecognition[1]:
                    flagCase(coords[1], coords[0])
                    lastAction="patter : flagged on : "+str(coords[1])+", "+str(coords[0])
                    if b.finished:
                        print("raté a cause du pattern")
        else:
            unknownList=[]
            for row in range(HEIGHT):
                for col in range(WIDTH):
                    if aiBoard[row][col]=="*":
                        unknownList.append([row, col])
            if len(unknownList)!=0:
                rd=random.choice(unknownList)
                canvas.event_generate('<Button-1>', x=rd[1]*SQUARE_SIZE+BORDER_SIZE+SQUARE_SIZE/2, y=rd[0]*SQUARE_SIZE+BORDER_SIZE+SQUARE_SIZE/2)
                lastAction="rng : clicked on : "+str(rd[1])+", "+str(rd[0])
            
    # If ai fail, reset here to gain time on the loops
    # otherwise, we need to wait for the next click, so the ai need to fill caseToCheck and a lot of other things
    if b.finished:
        if lastAction!=[]:
            print(lastAction)
        reset()
        startAI()
    else:
        window.after(AISPEED, ai)
   
startAI()

window.mainloop()