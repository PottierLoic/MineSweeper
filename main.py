# MineSweeper   
# Author : Loïc Pottier
# Creation date : 21/12/2022

# IMPORTS
import time
import random
import os

import copy
from tkinter import *
from PIL import Image, ImageTk

# other files from this project
import pattern
import board
from constants import *

# called by tk when the left click is used
# it change the case to discovered if it was unknown
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
# it change the case to flagged if it was unknown
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
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if b.oldBoard[y][x]!=b.supBoard[y][x]:
                canvas.delete(str(x)+" "+str(y))
                if b.supBoard[y][x]==1:
                    if b.board[y][x]=="x":
                        canvas.create_image(x*SQUARE_SIZE + BORDER_SIZE, y*SQUARE_SIZE+BORDER_SIZE, anchor="nw", image=bombImage, tag=("case", str(x)+" "+str(y)))
                    else:
                        canvas.create_image(x*SQUARE_SIZE + BORDER_SIZE, y*SQUARE_SIZE+BORDER_SIZE, anchor="nw", image=NUMBERS[b.board[y][x]], tag=("case", str(x)+" "+str(y)))
                elif b.supBoard[y][x]==0:
                    canvas.create_image(x*SQUARE_SIZE + BORDER_SIZE, y*SQUARE_SIZE+BORDER_SIZE, anchor="nw", image=hiddenImage, activeimage=overImage, tag=("case", str(x)+" "+str(y))) 
                else:
                    canvas.create_image(x*SQUARE_SIZE + BORDER_SIZE, y*SQUARE_SIZE+BORDER_SIZE, anchor="nw", image=flagImage, tag=("case", str(x)+" "+str(y)))
    b.oldBoard=copy.deepcopy(b.supBoard)
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
    b.reset()
    canvas.config(bg=BACKGROUND_COLOR)
    label.config(text="MineSweeper")

    if not AI_ON:
        discoverFirstCase()

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

# print the board in parameter in console, used for debug, I leave it here
def printBoard(b):
    os.system('cls')
    for row in b:
        for col in row:
            print(col, end=" ")
        print("")  
    print("")  

# STATS SECTION
# used at the end of the file 
victory=0
defeat=0
scores=[]
rngCount=0
rngCountTotal=0
patternRate=[]

#------------------------------------------------------------------------
# IA PART
#------------------------------------------------------------------------

# creating the board that the ai will analyze
aiBoard=[]

# fill the aiBoard with 0
# so we can update it when in the next function
def initAIBoard():
    global aiBoard
    aiBoard=[]
    for i in range(HEIGHT):
        aiBoard.append([])
        for _ in range(WIDTH):
            aiBoard[i].append(0)

# update the ai board using the sup and main board
# it only contain what a real player can see from the game
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
    return aiBoard

# remove fully discovered or unknown parts and return the new board and x, y starting pos
# we need them to fil the gap between the ai board and the cutted board
# not sure if it works well, toook 900sec vs 806 sec without for 200 games
def boardCutter():
    xStart=0
    newBoard=[]

    # find the starting line
    yStart=0
    for row in range(len(aiBoard)):
        if aiBoard[row].count("*")==len(aiBoard[row]):
            yStart=row
        else:
            break

    # do the same but starting from the end, and find the ending line
    yEnd=len(aiBoard)-1
    for row in range(len(aiBoard)-1, 0, -1):
        if aiBoard[row].count("*")==len(aiBoard[row]):
            yEnd=row
        else:
            break

    # if we removed nothing, we search for fully discovered parts
    if yStart==0:
        for row in range(len(aiBoard)):
            valid=True
            for value in aiBoard[row]:
                if value=="*" and valid:
                    valid=False

            if valid:
                yStart=row
            else:
                break

        if yStart!=0:
            yStart-=1

    # same but starting from the end
    if yEnd==len(aiBoard)-1:
        for row in range(len(aiBoard)-1, 0, -1):
            valid=True
            for value in aiBoard[row]:
                if value=="*" and valid:
                    valid=False
            if valid:
                yEnd=row
            else:
                break

    # x part here
    # find the starting collumn
    for value in range(len(aiBoard[0])):
        valid=True
        for row in range(len(aiBoard)):
            if aiBoard[row][value]!="*" and valid:
                valid=False
        if valid:
            xStart=value
        else:
            break

    xEnd=len(aiBoard[0])-1
    # do the same but starting from the end to find the ending value
    for value in range(len(aiBoard[0])-1, 0, -1):
        valid=True
        for row in range(len(aiBoard)):
            if aiBoard[row][value]!="*" and valid:
                valid=False
        if valid:
            xEnd=value
        else:
            break


    # if we can't remove unknown part, we try to remove discovered part
    # get the starting collumn
    if xStart==0:
        for value in range(len(aiBoard[0])):
            valid=True
            for row in range(len(aiBoard)):
                if aiBoard[row][value]=="*" and valid:
                    valid=False
            if valid:
                xStart=value
            else:
                break

        if xStart!=0:
            xStart-=1

    # do the same but starting from the end to find the ending value
    if xEnd==len(aiBoard[0])-1:
        for value in range(len(aiBoard[0])-1, 0, -1):
            valid=True
            for row in range(len(aiBoard)):
                if aiBoard[row][value]=="*" and valid:
                    valid=False
            if valid:
                xEnd=value
            else:
                break

    while xEnd-xStart<5:
        if xStart!=0:
            xStart-=1
        else:
            xEnd+=1
        print("x", xEnd, xStart, xEnd-xStart)

    while yEnd-yStart<5:
        if yStart!=0:
            yStart-=1
        else:
            yEnd+=1
        print("y", yEnd, yStart, yEnd-yStart)
    
    # add all the lines between yStart and xEnd and only values between xStart and xEnd
    for row in range(yStart, yEnd+1):
        newBoard.append(aiBoard[row][xStart:xEnd+1])

    return newBoard, xStart, yStart

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

lastAction=[]
# main ai
def ai():
    global rngCount, rngCountTotal
    aiBoard=updateAIBoard()
    needStop=False

    shiftX, shiftY = 0, 0
    aiBoard, shiftX, shiftY = boardCutter()
    printBoard(aiBoard)


    # FIRST PART
    # this part will try to solve the actual state by checking one case at a time
    # it will no take into account the others numbers around it
    # put all the cases filled with number other than 0 in a list
    caseToCheck=[]
    for y in range(len(aiBoard)):
        for x in range (len(aiBoard[y])):
            if aiBoard[y][x] not in ("*", 0, "~", "*"):
                valid=False
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if 0<=y+dy<len(aiBoard) and 0<=x+dx<len(aiBoard[0]):
                            if aiBoard[y+dy][x+dx]=="*":
                                valid=True
                if valid:
                    caseToCheck.append((y, x))

    # check around cases in caseToCheck if :
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
                if 0<=coords[0]<len(aiBoard) and 0<=coords[1]<len(aiBoard[0]):
                    if aiBoard[coords[0]][coords[1]]=="*":
                        unknown+=1
                        unknownList.append([coords[0], coords[1]])
                    elif aiBoard[coords[0]][coords[1]]=="~":
                        flagged+=1

            if type(aiBoard[case[0]][case[1]])==int:
                # if the number of flagged cases around is equal to the number on the actual case
                # it means that all the bombs are found, so we can click on every unknown cas
                if flagged==aiBoard[case[0]][case[1]]:
                    for unknownCase in unknownList:
                        clickCase(unknownCase[1]+shiftX, unknownCase[0]+shiftY)
                        lastAction.append("basic click : clicked on : "+str(unknownCase[1]+shiftX)+" "+str(unknownCase[0]+shiftY)) # to debug basic click error (when around case match the number of a case)
                    done=True
                            
                # if the number of unknown cases around is equal to the number on the actual case - flags around
                # we can juste flag every unknown case because there is 0% chance for them to be a bomb
                elif unknown==aiBoard[case[0]][case[1]]-flagged:
                    for unknownCase in unknownList:
                        flagCase(unknownCase[1]+shiftX, unknownCase[0]+shiftY)
                        lastAction.append("basic flag : flagged on : "+str(unknownCase[1]+shiftX)+" "+str(unknownCase[0]+shiftY)) # to debug basic flag error (when around case match the number of a case)
                    done=True

            #if game is finished, no need to continue
            # the ai can't fail here, standart click and flags are a 100% percent chance safe
            # BUT if a pattern has an error in it, this part can loose because the infos provided are wrong (a flag on a safe case for example)

            #TODO find a way to see if this corresponds to a victory or loose
            # if loose, need to print something because if this part fails, it is a pattern problem from the next part
            if b.finished:
                if b.checkLoose():
                    print("loose on a basic action ! CHECK PATTERNS")
                    needStop=True
                break

    # SECOND PART
    # Patter finder part
    # if the first part does not provide any single action to do, this part is the only way to continue the game
    # it will try to find patterns in the board that allow us to continue by taking into account groups of cases
    if not done:
        patternRecognition=pattern.patternFinder(aiBoard)
        if patternRecognition!=None:
            patternRate.append(patternRecognition[2])
            if patternRecognition[0]=="safe":
                for coords in patternRecognition[1]:
                    clickCase(coords[1]+shiftX, coords[0]+shiftY)
                    lastAction.append("pattern : clicked on : "+str(coords[1])+", "+str(coords[0])) #to debug pattern errors
            else:
                for coords in patternRecognition[1]:
                    flagCase(coords[1]+shiftX, coords[0]+shiftY)
                    lastAction.append("pattern : flagged on : "+str(coords[1]+shiftX)+", "+str(coords[0]+shiftY)) #to debug pattern errors
            done=True

    # THIRD PART
    # pattern reduction part
    # this part will reduce the board numbers by using the boardReducer function form pattern.py
    # it will substract the number of bombs around a number from its value and remove the bombs at the end
    # so we don't have to implement every possibiliy in the pattern section
    if not done:
        boardReduced=copy.deepcopy(pattern.boardReducer(copy.deepcopy(aiBoard)))
        patternRecognition=pattern.patternFinder(boardReduced)
        if patternRecognition!=None:
            patternRate.append(patternRecognition[2])
            if patternRecognition[0]=="safe":
                for coords in patternRecognition[1]:
                    clickCase(coords[1]+shiftX, coords[0]+shiftY)
                    lastAction.append("reduced pattern : clicked on : "+str(coords[1])+", "+str(coords[0])) #to debug reduced pattern errors
            else:
                for coords in patternRecognition[1]:
                    flagCase(coords[1]+shiftX, coords[0]+shiftY)
                    lastAction.append("reduced pattern : flagged on : "+str(coords[1]+shiftX)+", "+str(coords[0]+shiftY)) #to debug reduced pattern errors
            done=True

    # FOURTH PART
    # probability part, to be used in the last part of the game
    # it will calculate the probability of a case to be a bomb by using the number of bombs around it and the number of unknown cases around it
    # it will then click on the case with the lowest probability
    if not done:
        probBoard=[]
        for i in range(len(aiBoard)):
            probBoard.append([])
            for j in range(len(aiBoard[0])):
                probBoard[i].append([])

        for y in range(len(aiBoard)):
            for x in range (len(aiBoard[y])):
                if aiBoard[y][x] not in ("*", 0, "~", "*"):
                    valid=False
                    localUnknown=[]
                    flagged=0
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            if 0<=y+dy<len(aiBoard) and 0<=x+dx<len(aiBoard[0]):
                                if aiBoard[y+dy][x+dx]=="*":
                                    localUnknown.append((y+dy, x+dx))
                                    valid=True
                                elif aiBoard[y+dy][x+dx]=="~":
                                    flagged+=1
                    if valid:
                        toFind=aiBoard[y][x]-flagged
                        prob=len(localUnknown)/toFind
                        for unknown in localUnknown:
                            probBoard[unknown[0]][unknown[1]].append(prob)

        # we do the avg of each case
        for y in range(len(probBoard)):
            for x in range(len(probBoard[y])):
                if probBoard[y][x]!=[]:
                    probBoard[y][x]=sum(probBoard[y][x])/len(probBoard[y][x])
                else:
                    probBoard[y][x]=0
    
        # and get min value
        min=100
        probx=-1
        proby=-1
        for y in range(len(probBoard)):
            for x in range(len(probBoard[y])):
                if probBoard[y][x]<min and probBoard[y][x]!=0:
                    min=probBoard[y][x]
                    probx=x
                    proby=y

        # we click on the square with the lowest probability
        if probx!=-1 and proby!=-1:
            probx+=shiftX
            proby+=shiftY
            clickCase(probx, proby)
            done=True
            lastAction.append("prob : clicked on : "+str(probx)+", "+str(proby)) #to debug
            rngCountTotal+=1
            if b.finished:
                rngCount+=1
    
    # LAST PART
    # If the last squares have no numbers around them, we can just try a random click
    # that a pretty rare case, but it can happen
    if not done:
        unknownList=[]
        for row in range(len(aiBoard)):
            for col in range(len(aiBoard[0])):
                if aiBoard[row][col]=="*":
                    unknownList.append([row, col])
        if len(unknownList)!=0:
            rd=random.choice(unknownList)
            clickCase(rd[1], rd[0])
            lastAction.append("rng : clicked on : "+str(rd[1])+", "+str(rd[0])) #to debug

    # If ai fail, reset here to gain time on the loops
    # otherwise, we need to wait for the next click, so the ai need to fill caseToCheck and a lot of other things
    if b.finished:
        if lastAction!=[] and not b.checkWin():
            print(lastAction[-1])
        lastAction.clear()
        nb=0
        for row in b.supBoard:
            for col in row:
                if col==2:
                    nb+=1
        scores.append(MINE_AMOUNT-nb)
        if needStop and STOP_IF_FAIL:
            quit()
        reset()
        startAI()
    else:
        window.after(AISPEED, ai)
   


# AI START | WINDOW LOOP
if __name__=="__main__":

    # WINDOW AND TKINTER SECTION
    window = Tk()
    window.title("MineSweeper")
    window.resizable(False, False)

    label = Label(window, text="MineSweeper", font=("consolas", 10))
    label.pack()

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

    b = board.Board()

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

    graphics()

    startTime=time.time()

    startAI()

    window.mainloop()

    endTime=time.time()

    # STATISTIC PART | printed on window exit
    # patternFinder
    print("\n------------------")
    print("patterFinder stats")
    for name, p in pattern.patternList.items():
        print(f"{name:<10}{patternRate.count(name):<20}")
    print("------------------\n")

    # win/loose 
    a="Total victories : "
    b="Total defeats :   "
    print(f"{a:<15}{victory:<20}")
    print(f"{b:<15}{defeat:<20}")

    #probability clicks
    print("number of rng clicks that caused a defeat is : ", rngCount, " / ", rngCountTotal, "\n")

    # average score (nomber on unflagged bombs)
    avg=0
    if scores!=[]:
        for i in scores:
            avg+=i
        avg/=len(scores)
        print("average score of this session is : ", avg, "\n")
        print("wich mean that ", round(100-(avg/MINE_AMOUNT)*100, 2), "% of bombs have been found")

    print("duration of this session is : ", endTime-startTime)

