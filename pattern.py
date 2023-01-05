# Patterns for the minesweeper AI   
# Author : Loïc Pottier
# Creation date : 05/01/2023

# IMPORTS
import copy


# the patterList dictionnary contain patterns that the ai can use in its patterRecognition part
# the dict contains multiples dictionnaries that each have 3 items : pattern, bomb position and safe position

# first, the pattern part :
# a 2D list that contains str, a "!" means a discovered case and a "*" means an unknown one
# if it's a number, it represents the number on the case

# and the bombPos part :
# it is a list of coords, thoses are the relative positions that are bombs so the ai can right click on them

# each pattern has 4 rotations and 2 reversals, so the ai can check for all of them
# the name will be name, nameR, nameR2, nameR3, name' and name'R, name'R2, name'R3

# patterns implemented from https://minesweeper.online/help/patterns

# already done : 1-1, 1-1+, 1-2(don't need to do 1-2C)
# to add : 1-2+, 1-2-1, 1-2-2-1
# then reduction, holes, triangles, and some high complexity paterns
patternList={
    "1-1": {
        "pattern": [["!", "*", "*", "*"],
                    ["!", 1, 1, "!"],
                    ["!", "!", "!", "!"]],

        "bombPos": [], 
        "safePos": [[0, 3]]
    },

    "1-1R": {
        "pattern": [['*', '!', '!'], 
                    ['*', 1, '!'], 
                    ['*', 1, '!'], 
                    ['!', '!', '!']],

        "bombPos": [], 
        "safePos": [[0, 0]]
    },

    "1-1R2": {
        "pattern": [['!', '!', '!', '!'], 
                    ['!', 1, 1, '!'], 
                    ['*', '*', '*', '!']],

        "bombPos": [], 
        "safePos": [[2, 0]]
    },

    "1-1R3": {
        "pattern": [['!', '!', '!'], 
                    ['!', 1, '*'], 
                    ['!', 1, '*'], 
                    ['!', '!', '*']],

        "bombPos": [], 
        "safePos": [[3, 2]]
    },

    "1-1'": {
        "pattern": [['!', '!', '!', '!'], 
                    ['!', 1, 1, '!'], 
                    ['!', '*', '*', '*']],

        "bombPos": [], 
        "safePos": [[2, 3]]
    },

    "1-1'R1": {
        "pattern": [['!', '!', '*'], 
                    ['!', 1, '*'], 
                    ['!', 1, '*'],
                    ['!', '!', '!']],

        "bombPos": [], 
        "safePos": [[0, 2]]
    },

    "1-1'R2": {
        "pattern": [['*', '*', '*', '!'], 
                    ['!', 1, 1, '!'], 
                    ['!', '!', '!', '!']],

        "bombPos": [], 
        "safePos": [[0, 0]]
    },

    "1-1'R3": {
        "pattern": [['!', '!', '!'], 
                    ['*', 1, '!'], 
                    ['*', 1, '!'], 
                    ['*', '!', '!']],

        "bombPos": [], 
        "safePos": [[3, 0]]
    },

    "1-1+": {
        "pattern": [["!", "*", "*", "*"],
                    ["!", 1, 1, "*"],
                    ["!", "!", 1, "*"]],

        "bombPos": [], 
        "safePos": [[0, 3], [1, 3], [2, 3]]
    },

     "1-1+R1": {
        "pattern": [['*', '*', '*'], 
                    ['*', 1, 1], 
                    ['*', 1, '!'], 
                    ['!', '!', '!']],

        "bombPos": [], 
        "safePos": [[0, 0], [0, 1], [0, 2]]
    },

     "1-1+R2": {
        "pattern": [['*', 1, '!', '!'], 
                    ['*', 1, 1, '!'], 
                    ['*', '*', '*', '!']],

        "bombPos": [], 
        "safePos": [[0, 0], [1, 0], [2, 0]]
    },

     "1-1+R3": {
        "pattern": [['!', '!', '!'], 
                    ['!', 1, '*'], 
                    [1, 1, '*'], 
                    ['*', '*', '*']],

        "bombPos": [], 
        "safePos": [[3, 0], [3, 1], [3, 2]]
    },

    "1-1+'": {
        "pattern": [["!", "!", 1, "*"],
                    ["!", 1, 1, "*"],
                    ["!", "*", "*", "*"]],

        "bombPos": [], 
        "safePos": [[0, 3], [1, 3], [2, 3]]
    },

    "1-1+'R": {
        "pattern": [['*', '*', '*'], 
                    [1, 1, '*'], 
                    ['!', 1, '*'], 
                    ['!', '!', '!']],

        "bombPos": [], 
        "safePos": [[0, 0], [0, 1], [0, 2]]
    },

    "1-1+'R1": {
        "pattern": [['*', 1, '!', '!'], 
                    ['*', 1, 1, '!'], 
                    ['*', '*', '*', '!']],

        "bombPos": [], 
        "safePos": [[0, 0], [1, 0], [2, 0]]
    },

    "1-1+'R2": {
        "pattern": [['!', '!', '!'], 
                    ['!', 1, '*'], 
                    [1, 1, '*'], 
                    ['*', '*', '*']],

        "bombPos": [], 
        "safePos": [[3, 0], [3, 1], [3, 2]]
    },

    "1-2": {
        "pattern": [['*', '*', '*', '*'], 
                    ['!', 1, 2, "!"], 
                    ['!', '!', '!', '!']],

        "bombPos": [[0, 3]], 
        "safePos": []
    },

    "1-2R1": {
        "pattern": [['*', '!', '!'],
                    ['*', 2, '!'], 
                    ['*', 1, '!'], 
                    ['*', '!', '!']],

        "bombPos": [[0, 0]], 
        "safePos": []
    },

    "1-2R2": {
        "pattern": [['!', '!', '!', '!'], 
                    ['!', 2, 1, '!'],
                    ['*', '*', '*', '*']],

        "bombPos": [[2, 0]], 
        "safePos": []
    },

    "1-2R3": {
        "pattern": [['!', '!', '*'], 
                    ['!', 1, '*'], 
                    ['!', 2, '*'], 
                    ['!', '!', '*']],

        "bombPos": [[3, 2]], 
        "safePos": []
    },

    "1-2'": {
        "pattern": [['!', '!', '!', '!'], 
                    ['!', 1, 2, '!'], 
                    ['*', '*', '*', '*']],

        "bombPos": [[2, 3]], 
        "safePos": []
    },

    "1-2'R1": {
        "pattern": [['!', '!', '*'], 
                    ['!', 2, '*'], 
                    ['!', 1, '*'], 
                    ['!', '!', '*']],

        "bombPos": [[0, 2]], 
        "safePos": []
    },

    "1-2'R2": {
        "pattern": [['*', '*', '*', '*'], 
                    ['!', 2, 1, '!'], 
                    ['!', '!', '!', '!']],

        "bombPos": [[0, 0]], 
        "safePos": []
    },

    "1-2'R3": {
        "pattern": [['*', '!', '!'], 
                    ['*', 1, '!'], 
                    ['*', 2, '!'],
                    ['*', '!', '!']],

        "bombPos": [[3, 0]], 
        "safePos": []
    }
}


def rotatePattern(pattern):
    newPattern=[]
    for i in range(len(pattern[0])):
        newPattern.append([])
    for i in range(len(pattern[0])):
        for j in range(len(pattern)):
            newPattern[i].append(pattern[j][i])
    newPattern.reverse()
    return newPattern

def reversePattern(pattern):
    newPattern=[]
    for i in range(len(pattern)):
        newPattern.append([])
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            newPattern[i].append(pattern[i][j])
    newPattern.reverse()
    return newPattern

# pattern = patternList.get("1-2").get("pattern")
# reversed=reversePattern(pattern)
# print(reversed)

# reversed=rotatePattern(reversed)
# print(reversed)

# reversed=rotatePattern(reversed)
# print(reversed)

# reversed=rotatePattern(reversed)
# print(reversed)



# this function add a border of "!" to the board, so we can check for patters even if we are in y or x = 0
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
                                if board[row+dy][col+dx]=="*":
                                    pass
                                else:
                                    found=False
                            elif pattern[dy][dx]=="!" and found:
                                if board[row+dy][col+dx]!="*":
                                    pass
                                else:
                                    found=False
                            elif found:
                                if board[row+dy][col+dx]==pattern[dy][dx]:
                                    pass
                                else:
                                    found=False

                    if found:
                        print("found", name)
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
                return ["bomb", returnList]

            if safeList!=[]:
                for i in range(len(safeList)):
                    returnList.append([safeList[i][0]+y, safeList[i][1]+x])
                return ["safe", returnList]


# b=[
#     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
#     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
#     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
#     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
#     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
#     ['*', '*', "!", "*", "*", "*", '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
#     ['*', '*', "!",  1 ,  1 , "*", '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
#     ['*', '*', "!", "!",  1 , "*", '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
#     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
#     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
#     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
#     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
#     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
#     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
#     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
#     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
#     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
#     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
#     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
#     ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*']]


# b=boardTranslator(b)

# for i in b:
#     for j in i:
#         print(j, end=" ")
#     print("")

# print(patternFinder(b))