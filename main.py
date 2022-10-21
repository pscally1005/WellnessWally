import os
import getch

from nutritionLog import *
from bmiCalc import *
from paceCalc import *
from splitCalc import *

# Clears screen and prints the main menu title
def titlePrint():
    
    clear = lambda: os.system('clear')
    clear()

    print("##################")
    print("#                #")
    print("# WELLNESS WALLY #")
    print("#                #")
    print("##################")

# Prints the menu options
def optionsPrint():

    print()
    print("1: Nutrition Log")
    print("2: BMI Calculator")
    print("3: Pace Calculator")
    print("4: Split Calculator")
    print("X: Exit")
    print("Enter a number to select")

# User selects an option
def input():

    select = getch.getch()
    return select

# Takes to selected screen or prints error message
def selectOption(select):

    if select == "\r" or select == chr(27):
        print("\nYou selected: \'\'")
    else:
        print("\nYou selected: \'" + select + "\'")

    if select == "1":
        print("Launching Nutrition Log...")
        nutritionLog_main()
        return

    elif select == "2":
        print("Launching BMI Calculator...")
        bmi_main()
        return

    elif select == "3":
        print("Launching Pace Calculator...")
        pace_main()
        return

    elif select == "4":
        print("Launching Split Calculator...")
        split_main()
        return

    elif select == "X" or select == "x":
        print("Quitting now...")
        return

    print("ERROR: Input is invalid.  Please try again")
    select = getch.getch()
    titlePrint()
    optionsPrint()
    selectOption(select)

# Main function
def main():
    titlePrint()
    optionsPrint()
    select = input()
    selectOption(select)

if __name__ == "__main__" :
    main()