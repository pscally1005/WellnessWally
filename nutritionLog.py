import os
import getch
from datetime import date
from datetime import datetime

def nutritionLog_infoPrint(rating=-1):
    clear = lambda: os.system('clear')
    clear()

    print("NUTRITION LOG")
    print("\nThis will allow you to rate your nutrition for today and why")
    print("This data will be saved to a log file")

    print("\nPlease rate your nutrition for today from 1 to 5")

    if rating == -1: return
    print(rating)
    print("\nPlease describe why you rated your day as a \'" + rating + "\'")

# User enters their rating from 1-5
def nutritionLog_enterNum():
    nutritionLog_infoPrint()
    rating = getch.getch()

    if rating == "1" or rating == "2" or rating == "3" or rating == "4" or rating == "5":
        return rating
    else: return nutritionLog_enterNum()    

# User inputs their nutrition description
def nutritionLog_desc(rating):
    nutritionLog_infoPrint(rating)
    file = open("nutritionLog.txt", "a")
    desc = input()

    dt = datetime.now()
    dt = dt.strftime("%b-%d-%Y %H:%M:%S")
    dt = "[" + dt + "]: "

    file.write(dt + rating + " - " + desc + "\n")
    file.close()

    print("\nSaving...")
    print("\nEnter \'Y\' to to stay on this screen, or anything else to return")
    exit = getch.getch()

    if exit == "Y" or exit == "y": return nutritionLog_main()
    else: return

# Nutrition log main function
def nutritionLog_main():
    rating = nutritionLog_enterNum()
    nutritionLog_desc(rating)

if __name__ == "__main__" :
    nutritionLog_main()