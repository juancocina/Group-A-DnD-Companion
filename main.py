# Group A
# Stephen Lee
# Dice rolling module

import random

def numDie():
    num = input("How many die will you roll? ")
    return num

def sideDie():
    side = input("How many sides does your dice/die have? ")
    return side

def modifier():
    mod = input("Enter modifier value: ")
    return mod

def typeRoll(num, side):
    type = "{}d{}".format(num, side)
    return type

def rollDice(sides):
    result = random.randint(1, sides)
    return result

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    total = 0
    num = int(numDie())
    side = int(sideDie())
    mod = int(modifier())
    type = typeRoll(num, side)
    for x in range(num):
        roll = rollDice(side)
        print("Die #{}: {}".format(x+1, roll))
        total += roll
    total += mod
    print("{}: {}".format(type, total))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
