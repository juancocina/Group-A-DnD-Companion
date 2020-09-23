from tkinter import *
from tkinter import messagebox
from random import randint

# roll the dice
def roll(numEntry, sideEntry, modEntry):
    total = 0
    num = getEntry(numEntry)
    side = getEntry(sideEntry)
    mod = getEntry(modEntry)
    type = getType(num, side)
    for x in range(num):
        roll = rollDice(side)
        total += roll
    total += mod
    result.set("{}: {}".format(type, total))

# rolling die of n sides
def rollDice(sides):
    result = randint(1, sides)
    return result

def getEntry(entryWidget):
    entry = entryWidget.get()
    if entry.isdigit():
        return int(entry)
    else:
        return 0

# get type of dice
def getType(num, side):
    type = "{}d{}".format(num, side)
    return type

# create window
window = Tk()
window.title = ("Dice Roll")
window.geometry("400x200")

# create frames
numFrame = Frame(window)
numFrame.pack(fill = X)
sideFrame = Frame(window)
sideFrame.pack(fill = X)
modFrame = Frame(window)
modFrame.pack(fill = X)
textFrame = Frame(window)
textFrame.pack(fill = X)

# create label and entry for # of dice
numLabel = Label(numFrame, text="How many die?")
numLabel.pack(padx = 5, pady = 10, side = LEFT)
numEntry = Entry(numFrame)
numEntry.pack(padx = 5, pady = 10, side = LEFT)

# create label and entry for # of sides
sideLabel = Label(sideFrame, text="How many sides?")
sideLabel.pack(padx = 5, pady = 10, side = LEFT)
sideEntry = Entry(sideFrame)
sideEntry.pack(padx = 5, pady = 10, side = LEFT)

# create label and entry for modifier
modLabel = Label(modFrame, text="Modifier:")
modLabel.pack(padx = 5, pady = 10, side = LEFT)
modEntry = Entry(modFrame)
modEntry.pack(padx = 5, pady = 10, side = LEFT)

# create text to show result
result = StringVar()
text = Label(textFrame, textvariable = result)
result.set("Roll the Dice")
text.pack(pady = 10, side = BOTTOM)

# create button to roll dice
rollButton = Button(window, text="Roll", command=lambda : roll(numEntry, sideEntry, modEntry))
rollButton.pack(pady = 10, side = BOTTOM)

window.mainloop()