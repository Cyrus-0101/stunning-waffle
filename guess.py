#!/usr/bin/env python3
# +----------------------------------------------------------------------------------+ 
# | Since our code is running on multiple systems we include the first comment.      |
# | It is a Shebang line or Hashbang. Its a calling pattern for Unix based systems.  |
# | The #! must be included hence hash-bang, first two bytes in the file.            |
# | The Unix env path to find the Python Interpreter in the Machine.                 |
# +----------------------------------------------------------------------------------+

# Group 1 OOP2 - Guessing Game
import tkinter as tk
from random import randrange
# Game Initialization.
window = tk.Tk()
window.title("OOP2 - Guessing Game")
# Game labels.
lblInst = tk.Label(window, text = "Guess a number from 0 to 9")
lblLine0 = tk.Label(window, text = "*********************************************************************")
lblNoGuess = tk.Label(window, text = "No of Guesses: 0")
lblMaxGuess = tk.Label(window, text = "Max Guess: 3")
lblLine1 = tk.Label(window, text = "*********************************************************************")
lblLogs = tk.Label(window, text="Game Stats")
lblLine2 = tk.Label(window, text = "*********************************************************************")

# Create the buttons
buttons = []
for index in range(0, 10):
    # Here we assign all the buttons from 0, 10 using lambda functions. We disable the buttons by default before starting the game. 
    # We also pass the text widet to pass data.
    button = tk.Button(window, text=index, command=lambda index=index : process(index), state=tk.DISABLED)
    buttons.append(button)

# The game is either Started (Ready For A Restart) or not yet Started this is why we create an array to store this.
btnStartGameList = []
for index in range(0, 1):
    btnStartGame = tk.Button(window, text="Start Game", command=lambda : startgame(index))
    btnStartGameList.append(btnStartGame)

# Append elements to grid
lblInst.grid(row=0, column=0, columnspan=5)
lblLine0.grid(row=1, column=0, columnspan=5)
lblNoGuess.grid(row=2, column=0, columnspan=3)
lblMaxGuess.grid(row=2, column=3, columnspan=2)
lblLine1.grid(row=3, column=0, columnspan=5)
lblLogs.grid(row=4, column=0, columnspan=5)  # row 4 - 8 is reserved for showing game stats

lblLine2.grid(row=9, column=0, columnspan=5)

# Here we want to arrange all the numbers from 0 - 5 and
for row in range(0, 2):
    for col in range(0, 5):
        i = row * 5 + col  # convert 2d index to 1d. 5= total number of columns
        buttons[i].grid(row=row+10, column=col)
# Appending our vales to the 1st element in the array and assigning grid values, to the game mode.
btnStartGameList[0].grid(row=13, column=0, columnspan=5)

# Main game logic

guess = 0
totalNumberOfGuesses = 0
totalPoints = 20
secretNumber = randrange(10)
print(secretNumber)
lblLogs = [] # Here we want to be able to clear game stats on the game.
guess_row = 4
window.mainloop()
# reset all variables
def init():
    global buttons, guess, totalNumberOfGuesses, secretNumber, lblNoGuess, lblLogs, guess_row
    guess = 0
    totalNumberOfGuesses = 0
    secretNumber = randrange(10) # We chose randrange because it:
    # Chooses a random item from range(start, stop[, step]).
    # This fixes the problem with randint() which includes the endpoint; in Python this is usually not what you want.
    print(secretNumber)
    lblNoGuess["text"] = "Number of Guesses: 0"
    guess_row = 4

    # Remove all logs on init - So as to display the right message to the gamer
    for lblLog in lblLogs:
        lblLog.grid_forget()
    lblLogs = []

# Starting the game.
def process(i):
    global totalNumberOfGuesses, buttons, guess_row, totalPoints
    guess = i
    # Everytime a user guesses the value is appended and shown to the user with the following fn.
    totalNumberOfGuesses += 1
    lblNoGuess["text"] = "Number of Guesses: " + str(totalNumberOfGuesses)

    # Check if guess matches the secret number
    if guess == secretNumber:
        lbl = tk.Label(window, text="Your guess was right. You won! :) and got %d Points" % totalPoints, fg="green")
        lbl.grid(row=guess_row, column=0, columnspan=5)
        lblLogs.append(lbl)
        guess_row += 1

        # TODO: Work on points assigning dynamically.

        # Disabling the buttons that are selected.
        for b in buttons:
            b["state"] = tk.DISABLED
    else:
        # Give player some hints
        if guess > secretNumber:
            lbl = tk.Label(window, text="Secret number is less than your current guess :)", fg="red")
            lbl.grid(row=guess_row, column=0, columnspan=5)
            lblLogs.append(lbl)
            guess_row += 1

        # TODO: Checking if the guess is divisible by the number.
        else:
            lbl = tk.Label(window, text="Secret number is greater than your current guess :)", fg="red")
            lbl.grid(row=guess_row, column=0, columnspan=5)
            lblLogs.append(lbl)
            guess_row += 1

    # Game is over when max no of guesses is reached
    if totalNumberOfGuesses == 3:
        if guess != secretNumber:
            totalPoints = 0
            lbl = tk.Label(window, text="Max guesses reached. You lost :( and got %d points." % totalPoints, fg="red")
            lbl.grid(row=guess_row, column=0, columnspan=5)
            lblLogs.append(lbl)
            guess_row += 1

        for b in buttons:
            b["state"] = tk.DISABLED

    buttons[i]["state"] = tk.DISABLED 
    # Disable all buttons when game is complete.

# Waiting for a session to begin.
status = "none"

def startgame(i):
    global status
    for b in buttons:
        # Here we tell Tkinter to reverse the status of our buttons to normal so a user can begin the game.
        b["state"] = tk.NORMAL
    # Changing the status of the game to started. Users can restart the game at any time.
    if status == "none":
        status = "started"
        # Here we now append the "Restart Game" to btnStartGameList Array to add a Restart Game Feature once the game has been started.
        btnStartGameList[i]["text"] = "Restart Game"
    else:
        status = "restarted"
        # Start the game
        init()
    print("Game started")


def main():
    window.mainloop()

if __name__ == "__main__":
    main()