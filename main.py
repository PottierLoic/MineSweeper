# MineSweeper   
# Author : Loïc Pottier
# Creation date : 21/12/2022

# IMPORTS
from tkinter import *
from PIL import Image, ImageTk
import random

# CONSTANTS
BACKGROUND_COLOR = "#E0E0E0"
MINE_AMOUNT=100
HEIGHT=30
WIDTH=30
SQUARE_SIZE=20
BORDER_SIZE=10
NUMBERS=["img/0.png", "img/1.png", "img/2.png", "img/3.png", "img/4.png", "img/5.png", "img/6.png", "img/7.png", "img/8.png"]


class Board():
    def __init__(self):
        self.board=[]

        # Creation and filling of the main board with 0
        for i in range(HEIGHT):
            self.board.append([])
            for j in range(WIDTH):
                self.board[i].append(0)

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
                        if 0<=coords[1]<WIDTH and 0<=coords[0]<HEIGHT:
                            if self.board[coords[0]][coords[1]]=="x":
                                bombs+=1

                    self.board[y][x]=bombs
                      
                      
    def showRevealed(self):
        imgList=[]
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.board[y][x]=="x":
                    imgList.append(ImageTk.PhotoImage(Image.open("img/bomb.png").resize((SQUARE_SIZE, SQUARE_SIZE))))
                else:
                    imgList.append(ImageTk.PhotoImage(Image.open(NUMBERS[self.board[y][x]]).resize((SQUARE_SIZE, SQUARE_SIZE))))
                
                canvas.create_image(x*SQUARE_SIZE + BORDER_SIZE, y*SQUARE_SIZE+BORDER_SIZE, anchor="nw", image=imgList[-1])
        print(imgList)

    def __str__(self) -> str:
        r=""
        for y in range(HEIGHT):
            for x in range(WIDTH):
                r+=str(self.board[y][x])+" "
            r+="\n"
        return r


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



imgList=[]
for y in range(HEIGHT):
    for x in range(WIDTH):
        if b.board[y][x]=="x":
            imgList.append(ImageTk.PhotoImage(Image.open("img/bomb.png").resize((SQUARE_SIZE, SQUARE_SIZE))))
        else:
            imgList.append(ImageTk.PhotoImage(Image.open(NUMBERS[b.board[y][x]]).resize((SQUARE_SIZE, SQUARE_SIZE))))

        canvas.create_image(x*SQUARE_SIZE + BORDER_SIZE, y*SQUARE_SIZE+BORDER_SIZE, anchor="nw", image=imgList[-1])
print(imgList)



window.mainloop()