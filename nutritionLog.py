import os
import getch
from datetime import date
from datetime import datetime

# Prints nutrition log header message
def nutritionLog_header():

    clear = lambda: os.system('clear')
    clear()

    print("NUTRITION LOG")
    print("\nThis will allow you to rate your nutrition for today amd why")
    print("This data will be saved to a log file")

    print("\nPlease rate your nutrition for today from 1 to 5")

# User enters their rating from 1-5
def nutritionLog_enterNum():
    rating = getch.getch()
    return rating

# Checks if the users rating is valid
def nutritionLog_checkInput(rating):

    if rating == "\r" or rating == chr(27):
        print("\nYou entered: \'\'")
    else:
        print("\nYou entered: \'" + rating + "\'")

    if rating == "1" or rating == "2" or rating == "3" or rating == "4" or rating == "5":
        print("\nPlease describe why you rated your day as a \'" + rating + "\'\n")
        return
    
    print("ERROR: Input is invalid.  Please try again")
    rating = getch.getch()
    nutritionLog_header()
    nutritionLog_checkInput(rating)

# User inputs their nutrition description
def nutritionLog_desc(rating):

    file = open("nutritionLog.txt", "a")
    desc = input()

    dt = datetime.now()
    dt = dt.strftime("%b-%d-%Y %H:%M:%S")
    dt = "[" + dt + "]: "

    file.write(dt + rating + " - " + desc + "\n")
    file.close()

# Gives user option to return to main menu or stay on screen
def nutritionLog_end():

    print("\nSaving...")
    print("\nEnter \'Y\' to to stay on this screen, or anything else to return")
    exit = getch.getch()

    if exit == "Y" or exit == "y":
        return nutritionLog_main()
    else:
        return

# Nutrition log main function
def nutritionLog_main():
    nutritionLog_header()
    rating = nutritionLog_enterNum()
    nutritionLog_checkInput(rating)
    nutritionLog_desc(rating)
    nutritionLog_end()

if __name__ == "__main__" :
    nutritionLog_main()