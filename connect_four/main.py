# Title: Connect 4
# Author: Gabe Ponce, Sam Cook, Aidan David-Leforte, Jordan Kelsey
# Date: December 1, 2023
# filename: main.py
# Purpose: To play Connect 4 against the Computer

import time
import turtle
from turtle import Turtle, Screen
import random

STARTING_POSITION = (-150, 180)
XCOR_POSITIONS = [(-150, 180), (-100, 180), (-50, 180), (0, 180), (50, 180), (100, 180), (150, 180)]

# - using a matrix with the coordinates of the chip slots
# - running a count for the consecutive checking the entire board
# - check by moving up down or both (for diagonal) to check and if four consecutive return winner
mrx = [[(-150, 125), (-100, 125), (-50, 125), (0, 125), (50, 125), (100, 125), (150, 125)],
       [(-150, 75), (-100, 75), (-50, 75), (0, 75), (50, 75), (100, 75), (150, 75)],
       [(-150, 25), (-100, 25), (-50, 25), (0, 25), (50, 25), (100, 25), (150, 25)],
       [(-150, -25), (-100, -25), (-50, -25), (0, -25), (50, -25), (100, -25), (150, -25)],
       [(-150, -75), (-100, -75), (-50, -75), (0, -75), (50, -75), (100, -75), (150, -75)],
       [(-150, -125), (-100, -125), (-50, -125), (0, -125), (50, -125), (100, -125), (150, -125)]]


def check_if_winner(color):
    # Vertical row checking (Horizontal Win)
    for r in range(6):
        for c in range(4):
            if (mrx[r][c] == color and mrx[r][c + 1] == color and mrx[r][c + 2] == color and
                    mrx[r][c + 3] == color):
                return color
    # Horizontal row checking (Vertical Win)
    for x in range(3):
        for y in range(7):
            if (mrx[x][y] == color and mrx[x + 1][y] == color and mrx[x + 2][y] == color and
                    mrx[x + 3][y] == color):
                return color
    # Diagonal checking (Goes from top left covering the first three rows)
    for i in range(3):
        for z in range(4):
            if (mrx[i][z] == color and mrx[i + 1][z + 1] == color and mrx[i + 2][z + 2] == color and
                    mrx[i + 3][z + 3] == color):
                return color
    # Diagonal checking (goes from bottom left )
    for d in range(5, 2, -1):
        for c in range(4):
            if (mrx[d][c] == color and mrx[d - 1][c + 1] == color and mrx[d - 2][c + 2] == color and
                    mrx[d - 3][c + 3] == color):
                return color


def board_numbering():
    num1 = Turtle()
    num1.penup()
    num1.hideturtle()
    num1.goto(-150, -180)
    num1.write("1", align="center", font=('Helvetica', 15, 'bold'))
    num1.goto(-100, -180)
    num1.write("2", align="center", font=('Helvetica', 15, 'bold'))
    num1.goto(-50, -180)
    num1.write("3", align="center", font=('Helvetica', 15, 'bold'))
    num1.goto(0, -180)
    num1.write("4", align="center", font=('Helvetica', 15, 'bold'))
    num1.goto(50, -180)
    num1.write("5", align="center", font=('Helvetica', 15, 'bold'))
    num1.goto(100, -180)
    num1.write("6", align="center", font=('Helvetica', 15, 'bold'))
    num1.goto(150, -180)
    num1.write("7", align="center", font=('Helvetica', 15, 'bold'))

def game_screen():
    # Creates connect 4 board
    screen = Screen()
    screen.setup(width=600, height=600)
    screen.title("Connect 4 Game")
    board_numbering()
    screen.register_shape("connect4Fixed.gif")
    board = Turtle("connect4Fixed.gif")
    return screen


def GameState():
    # Gets game stats from document
    with open("game_stats.txt", "r") as file:
        doc = file.read()
        file.close()
        doc_list = doc.split(":")
        victories = int(doc_list[1])
        losses = int(doc_list[3])
        return victories, losses


def writeGameStats(winner, victories, losses):
    # Updates game stats
    if winner == "red":
        victories += 1
    if winner == "yellow":
        losses += 1
    # File path
    file_path = "game_stats.txt"
    # Writing to file
    with open(file_path, "w") as file:
        file.write(f"Victories: {victories} : Losses: {losses}\n")
        file.close()
    print(f"Data written to {file_path}")


def new_turtle(color, row_drop, column, screen):
    # Create new turtle and send it to position
    chip = Turtle("circle")
    chip.hideturtle()
    chip.shapesize(stretch_wid=2.2, stretch_len=2.2)
    chip.color(color)
    chip.penup()
    chip.goto(STARTING_POSITION)
    chip.showturtle()
    chip.speed("slow")
    chip.goto(XCOR_POSITIONS[column])
    chip.goto(mrx[row_drop][column])


def comp_turn():
    # Computers turn
    comp_color = "yellow"
    drop_column = random.randint(0, 6)
    comp_col = int(drop_column)
    comp_col -= 1
    # Check if the column is full
    while mrx[0][comp_col] == "yellow" or mrx[0][comp_col] == "red":
        drop_column = random.randint(0, 6)
        comp_col = int(drop_column)
        comp_col -= 1
    # Determine next empty row in column
    row = 5
    for num in range(6):
        if mrx[num][comp_col] == "yellow" or mrx[num][comp_col] == "red":
            row -= 1
    return comp_col, comp_color, row


def user_turn(screen):
    # User turn
    user_color = "red"
    drop_column = screen.numinput("Pick a Column", "Choose a number from 1 - 7", minval=1, maxval=7)
    if drop_column is None:
        quit()
    col_num = int(drop_column)
    col_num -= 1
    # Check if the column is full
    while mrx[0][col_num] == "yellow" or mrx[0][col_num] == "red":
        drop_column = screen.numinput("Column Full ", "Choose a number from 1 - 7", minval=1, maxval=7)
        if drop_column is None:
            quit()
        col_num = int(drop_column)
        col_num -= 1
    # Determine next empty row in column
    row = 5
    for num in range(6):
        if mrx[num][col_num] == "yellow" or mrx[num][col_num] == "red":
            row -= 1
    return col_num, user_color, row

def gameloop(screen):
    # Allow for turns up to maximum slots
    victories, losses = GameState()
    turns = 1
    for turn in range(1, 43):
        if turns % 2 == 0:
            col_num, color, row = comp_turn()
        else:
            col_num, color, row = user_turn(screen)
        turns += 1
        new_turtle(color, row_drop=row, column=col_num, screen=screen)
        mrx[row][col_num] = color
        winner = check_if_winner(color)
        if winner == "red":
            message = Turtle()
            message.hideturtle()
            message.penup()
            message.goto(0, 200)
            message.write("You WIN!\nGame Closing in 5 seconds", align="center", font=('Helvetica', 15, 'bold'))
            writeGameStats(winner, victories, losses)
            time.sleep(5)
            quit()
        if winner == "yellow":
            message = Turtle()
            message.hideturtle()
            message.penup()
            message.goto(0, 200)
            message.write("Computer WINS!\nGame Closing in 5 seconds", align="center", font=('Helvetica', 15, 'bold'))
            writeGameStats(winner, victories, losses)
            time.sleep(5)
            quit()


def displayInstructions():
    turtle.speed(100)
    turtle.penup()
    turtle.hideturtle()
    turtle.goto(-330, 275)
    turtle.color('yellow', 'ghostwhite')
    turtle.penup()
    turtle.begin_fill()
    turtle.left(90)
    turtle.forward(550)
    turtle.left(90)
    turtle.forward(655)
    turtle.left(90)
    turtle.forward(550)
    turtle.end_fill()

    turtle.penup()
    turtle.goto(-260, 150)
    turtle.write('INSTRUCTIONS', font=('Helvetica', 50, 'bold'))
    turtle.color('red')
    turtle.goto(-257, 147)
    turtle.write('INSTRUCTIONS', font=('Helvetica', 50, 'bold'))

    # draw background for instructions text

    turtle.penup()
    turtle.color('red')
    turtle.goto(-260, 140)
    turtle.begin_fill()
    turtle.right(90)
    turtle.forward(500)
    turtle.right(90)
    turtle.forward(320)
    turtle.right(90)
    turtle.forward(500)
    turtle.end_fill()

    turtle.penup()
    turtle.goto(-252, 100)
    turtle.color('yellow')
    turtle.write('The object of the game is to connect', font=('Helvetica', 20, 'bold'))
    turtle.goto(-252, 70)
    turtle.write('four chips by dropping them into a', font=('Helvetica', 20, 'bold'))
    turtle.goto(-252, 40)
    turtle.write('7 X 6 grid. Playing against the CPU,', font=('Helvetica', 20, 'bold'))
    turtle.goto(-252, 10)
    turtle.write('take turns dropping chips into the', font=('Helvetica', 20, 'bold'))
    turtle.goto(-252, -20)
    turtle.write('the top of different columns, and', font=('Helvetica', 20, 'bold'))
    turtle.goto(-252, -50)
    turtle.write('try to connect four of your chips', font=('Helvetica', 20, 'bold'))
    turtle.goto(-252, -80)
    turtle.write('together in a vertical, horizontal, or', font=('Helvetica', 20, 'bold'))
    turtle.goto(-252, -110)
    turtle.write('diagonal line. Enter a number from', font=('Helvetica', 20, 'bold'))
    turtle.goto(-252, -140)
    turtle.write('1 to 7 corresponding with the', font=('Helvetica', 20, 'bold'))
    turtle.goto(-252, -170)
    turtle.write('columns. Press OK or enter to drop.', font=('Helvetica', 20, 'bold'))

    # draw back button

    turtle.color('red')
    turtle.goto(-100, -200)
    turtle.begin_fill()
    turtle.right(180)
    turtle.forward(200)
    turtle.right(90)
    turtle.forward(50)
    turtle.right(90)
    turtle.forward(200)
    turtle.end_fill()

    turtle.penup()
    turtle.goto(-40, -242)
    turtle.color('yellow')
    turtle.write('BACK', font=('Helvetica', 20, 'bold'))

    # function to check for clicks

    def clickBack(x, y):
        if (x > -100 and x < 100 and y > -250 and y < -200):
            turtle.goto(-330, 275)
            turtle.right(180)
            homeScreen()

    turtle.onscreenclick(clickBack, 1)
    turtle.listen()

    turtle.done()


def homeScreen():
    turtle.speed(100)
    turtle.penup()
    turtle.hideturtle()
    turtle.goto(-330, 275)
    turtle.color('yellow', 'ghostwhite')
    turtle.penup()
    turtle.begin_fill()
    turtle.right(90)
    turtle.forward(550)
    turtle.left(90)
    turtle.forward(655)
    turtle.left(90)
    turtle.forward(550)
    turtle.end_fill()

    turtle.penup()
    turtle.goto(-240, 30)
    turtle.write('connect Four', font=('Helvetica', 60, 'normal'))
    turtle.color('red')
    turtle.goto(-237, 27)
    turtle.write('connect Four', font=('Helvetica', 60, 'normal'))

    turtle.color('red')
    turtle.goto(-270, -40)
    turtle.begin_fill()
    turtle.right(90)
    turtle.forward(200)
    turtle.right(90)
    turtle.forward(50)
    turtle.right(90)
    turtle.forward(200)
    turtle.end_fill()

    turtle.penup()
    turtle.goto(-260, -83)
    turtle.color('yellow')
    turtle.write('START GAME', font=('Helvetica', 20, 'bold'))

    turtle.color('red')
    turtle.goto(65, -40)
    turtle.begin_fill()
    turtle.left(180)
    turtle.forward(220)
    turtle.right(90)
    turtle.forward(50)
    turtle.right(90)
    turtle.forward(220)
    turtle.end_fill()

    turtle.penup()
    turtle.goto(71, -83)
    turtle.color('yellow')
    turtle.write('INSTRUCTIONS', font=('Helvetica', 20, 'bold'))

    turtle.color('red')
    turtle.goto(-110, -170)
    turtle.begin_fill()
    turtle.left(180)
    turtle.forward(220)
    turtle.right(90)
    turtle.forward(50)
    turtle.right(90)
    turtle.forward(220)
    turtle.end_fill()

    turtle.penup()
    turtle.goto(-75, -212)
    turtle.color('yellow')
    turtle.write('EXIT GAME', font=('Helvetica', 20, 'bold'))

    def clickStart(x, y):
        if (x > -270 and x < -70 and y > -90 and y < -40):
            turtle.clearscreen()
            game = game_screen()
            gameloop(screen=game)
        elif (x > 65 and x < 285 and y > -90 and y < -40):
            turtle.goto(-330, 275)
            displayInstructions()
        elif (x > -110 and x < 110 and y > -220 and y < -170):
            exit()

    turtle.onscreenclick(clickStart, 1)
    turtle.listen()

    turtle.done()


homeScreen()

# WE DID IT
