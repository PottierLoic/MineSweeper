# Patterns for the minesweeper AI   
# Author : Loïc Pottier
# Creation date : 05/01/2023

# IMPORTS
import copy
import json

# the patterList dictionnary contain patterns that the ai can use in its patterRecognition part
# the dict contains multiples dictionnaries that each have 3 items : pattern, bomb position and safe position

# first, the pattern part :
# a 2D list that contains str, a "!" means a discovered case and a "*" means an unknown one
# if it's a number, it represents the number on the case, of course, it is discovered

# and the bombPos and safePos parts :
# it is a list of coords, thoses are the relative positions that are bombs or safe places so the ai can flag/click on them

# each pattern has 4 rotations and 2 reversals, so the ai can check for all of them (edit : some are useless so i removed them)
# the name will be name, nameR, nameR2, nameR3, name' and name'R, name'R2, name'R3

# patterns implemented from https://minesweeper.online/help/patterns
# already done : 1-1, 1-1+, 1-2(don't need to do 1-2C), 1-2+
# 1-2-1 pattern is useless because it just use the basic 1-2 and basic checks of part 1 will unlock the problem
# 1-2-2-1 is the same, it use juste 1-2 and after it can find everything wth the basic check of part 1

# the reduction par is not made with patterns but with boardReducer, 
# it just subtract to number the amount of flagged cases around, and remove bombs from the board by putting 0 instead
# then make a new board with them, that is ready to be put in pattern finder
# holes, triangles, and some high complexity paterns

# load patterns from patterList.json
with open('patternList.json') as pattern:
    patternList = json.load(pattern)

with open('patternListTest.json') as pattern:
    patternListTest = json.load(pattern)

# this function add a border of "!" to the board, so we can check for patters even if we are in y or x == 0
def boardTranslator(board):
    newBoard=copy.deepcopy(board)
    lenght=len(board[0])
    newBoard.insert(0, [])
    newBoard.append([])
    for i in range(lenght):
        newBoard[0].append("!")
    for i in range(lenght+2):
        newBoard[-1].append("!")
    for row in range(len(newBoard)-1):
        newBoard[row].insert(0, "!")
        newBoard[row].append("!")
    return newBoard

# patterFinder will search in the board if there is a pattern for the patternList matching
# if so, it will return the bombPosition associated with the pattern
def patternFinder(board):
    board=boardTranslator(board)
    for name, p in patternList.items():
        pattern=p.get("pattern")
        bombsList=p.get("bombPos")
        safeList=p.get("safePos")
        yrange=len(board)-len(pattern)
        xrange=len(board[0])-len(pattern[0])
        found=True
        end=False
        x, y = 0, 0
        if not end:
            for row in range(yrange):
                for col in range(xrange):
                    found=True
                    for dy in range(len(pattern)):
                        for dx in range(len(pattern[0])):
                            if pattern[dy][dx]=="*" and found:
                                if board[row+dy][col+dx]!="*":
                                    found=False
                            elif pattern[dy][dx]=="!" and found:
                                if board[row+dy][col+dx] in ("*", "~"):
                                    found=False
                            elif found:
                                if board[row+dy][col+dx]!=pattern[dy][dx]:
                                    found=False

                    if found:
                        print("found ",name, " on ", col, row)
                        y, x = row-1, col-1
                        end=True
                        break

                if found:
                    break
   
        if found:
            returnList=[]
            if bombsList!=[]:
                for i in range(len(bombsList)):
                    returnList.append([bombsList[i][0]+y, bombsList[i][1]+x])
                return ["bomb", returnList, name]

            if safeList!=[]:
                for i in range(len(safeList)):
                    returnList.append([safeList[i][0]+y, safeList[i][1]+x])
                return ["safe", returnList, name]

# not working well
def patternFinderTest(board):
    board=boardTranslator(board)
    for name, p in patternListTest.items():
        pattern=p.get("pattern")
        bombsList=p.get("bombPos")
        safeList=p.get("safePos")
        yrange=len(board)-len(pattern)+1
        xrange=len(board[0])-len(pattern[0])+1
        found=True
        end=False
        x, y = 0, 0
        if not end:
            for row in range(yrange):
                for col in range(xrange):
                    found=True
                    unknownFound=False
                    for dy in range(len(pattern)):
                        for dx in range(len(pattern[0])):
                            if pattern[dy][dx]=="?":
                                if board[row+dy][col+dx]=="*":
                                    unknownFound=True
                            if pattern[dy][dx]=="*" and found:
                                if board[row+dy][col+dx]=="~":
                                    found=False
                            elif pattern[dy][dx]=="!" and found:
                                if board[row+dy][col+dx] in ("*", "~"):
                                    found=False
                            elif found:
                                if board[row+dy][col+dx]!=pattern[dy][dx]:
                                    found=False
                    if found:
                        if unknownFound:
                            validPos=False
                            if bombsList!=[]:
                                for coords in bombsList:
                                    if board[coords[0]+row][coords[1]+col]=="*":
                                        validPos=True
                            if safeList!=[]:
                                for coords in safeList:
                                    if board[coords[0]+row][coords[1]+col]=="*":
                                        validPos=True

                            if validPos:
                                print("found ",name, " on ", col, row)
                                y, x = row-1, col-1
                                end=True
                                break
                            else:
                                found=False

                if found:
                    break
            if found:
                break
        if found:
            returnList=[]
            if bombsList!=[]:
                for i in range(len(bombsList)):
                    returnList.append([bombsList[i][0]+y, bombsList[i][1]+x])
                return ["bomb", returnList, name]

            if safeList!=[]:
                for i in range(len(safeList)):
                    returnList.append([safeList[i][0]+y, safeList[i][1]+x])
                return ["safe", returnList, name]

# this function work BUT this is not a good solution, we can't use all patterns with this
# boardReducer substract to all numbers with unknown tiles around the number of flags around them
def boardReducer(board):
    newBoard=[]
    for y in range(len(board)):
        newBoard.append([])
        for x in range(len(board[0])):
            if type(board[y][x])==int:
                # List of pos to check for flags
                flags=0
                toCheck=[]
                unknownDetected=False
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        toCheck.append([y+dy, x+dx])
                # check flag presence in each position around actual pos
                for coords in toCheck:
                    if 0<=coords[0]<len(board) and 0<=coords[1]<len(board[0]):
                        if board[coords[0]][coords[1]]=="~":
                            flags+=1
                        if board[coords[0]][coords[1]]=="*":
                            unknownDetected=True
                
                if unknownDetected:
                    newBoard[y].append(board[y][x]-flags)
                else:
                    newBoard[y].append(board[y][x])
            else:
                if board[y][x]=="~":
                    newBoard[y].append(0)
                else:
                    newBoard[y].append(board[y][x])
    return newBoard
                

# used to turn pattern by 90°, just to create them faster, not used by other functions
def rotatePattern(pattern):
    newPattern=[]
    for i in range(len(pattern[0])):
        newPattern.append([])
    for i in range(len(pattern[0])):
        for j in range(len(pattern)):
            newPattern[i].append(pattern[j][i])
    newPattern.reverse()
    return newPattern

# same as rotate
def reversePattern(pattern):
    newPattern=[]
    for i in range(len(pattern)):
        newPattern.append([])
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            newPattern[i].append(pattern[i][j])
    newPattern.reverse()
    return newPattern

