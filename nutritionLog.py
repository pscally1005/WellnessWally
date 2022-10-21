import os
import getch

# Prints nutrition log header message
def nutritionLog_header():

    clear = lambda: os.system('clear')
    clear()

    print("NUTRITION LOG")
    print("\nRate your nutrition today from 1 to 5")

# Nutrition log main function
def nutritionLog_main():
    nutritionLog_header()

if __name__ == "__main__" :
    nutritionLog_main()