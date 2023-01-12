# constants for minesweeper   
# Author : Loïc Pottier
# Creation date : 10/01/2022

# CONSTANTS
BACKGROUND_COLOR = "#E0E0E0"
WIN_COLOR = "#00FF00"
LOOSE_COLOR = "#FF0000"

MINE_AMOUNT=80

HEIGHT=20
WIDTH=20

SQUARE_SIZE=10
BORDER_SIZE=10

# set this to false to desactivate AI and play yourself
AI_ON = True

# lower the speed is, faster the ia is, it represent the time waited between every action, so the tkinter interface can follow
AISPEED=1

# stop the game if the ai fail on a basic clic, usefull to check pattern validity
STOP_IF_FAIL=False

# set this to false to desactivate graphics updates, ai is faster with cli
UPDATE_GRAPHICS=True