import os
import getch

# Prints nutrition log header message
def nutritionLog_header():

    clear = lambda: os.system('clear')
    clear()

    print("NUTRITION LOG")
    #print("\nThis will allow you to rate your nutrition for today")

# Nutrition log main function
def nutritionLog_main():
    nutritionLog_header()

if __name__ == "__main__" :
    nutritionLog_main()