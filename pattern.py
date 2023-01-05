# Patterns for the minesweeper AI   
# Author : Loïc Pottier
# Creation date : 05/01/2023

# IMPORTS
import copy


# the patterList dictionnary contain patterns that the ai can use in its patterRecognition part
# the dict contains multiples dictionnaries that each have 2 items : pattern and bomb position

# first, the pattern part :
# a 2D list that contains str, a "!" means a discovered case and a "*" means an unknown one
# if it's a number, it represents the number on the case

# and the bombPos part :
# it is a list of coords, thoses are the relative positions that are bombs so the ai can right click on them
patternList={
    "1-1": {
        "pattern": [["!", "*", "*", "*"],
                    ["!", 1, 1, "!"],
                    ["!", "!", "!", "!"]],

        "bombPos": [[0, 3]]
    }
}


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

# patterFinder will search in the board if there is a patter for the patternList matching
# if so, it will return the bombPosition associated with the pattern
def patternFinder(board):
    print("recherche")
    board=boardTranslator(board)
    for name, p in patternList.items():
        pattern=p.get("pattern")
        coordsList=p.get("bombPos")
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
                            if pattern[dy][dx]=="*":
                                if board[row+dy][col+dx]=="*":
                                    pass
                                else:
                                    found=False
                            elif pattern[dy][dx]=="!":
                                if board[row+dy][col+dx]!="*":
                                    pass
                                else:
                                    found=False
                                print("check ! : ", found)
                            else:
                                if board[row+dy][col+dx]==pattern[dy][dx]:
                                    pass
                                else:
                                    found=False
                                print("check numbers : ", found)


                            
                            
                            #  and board[row+dy][col+dx]=="*":
                            #     pass
                            # elif pattern[dy][dx]=="!" and board[row+dy][col+dx]!="*":
                            #     pass
                            # elif type(pattern[dy][dx])==int and pattern[dy][dx]==board[row+dy][col+dx]:
                            #     pass
                            # else:
                            #     found=False

                    if found:
                        end=True
                        x, y = row, col
                        break

                if found:
                    break

            if found:
                for i in range(len(coordsList)-1):
                    coordsList[i][0]+=y
                    coordsList[i][1]+=x
                return coordsList

b=[
    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
    ['*', '*', 1, '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
    ['*', '*', 1, 1, 1, 5, '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
    ['*', '*', 1, 1, 1, 1, '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
    ['*', '*', '*', '*', "!", "*", "*", "*", '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
    ['*', '*', '*', '*', "!", 1, 1, "!", '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
    ['*', '*', '*', '*', "!", "!", "!", "!", '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
    ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*']]


b=boardTranslator(b)

for i in b:
    for j in i:
        print(j, end=" ")
    print("")

print(patternFinder(b))