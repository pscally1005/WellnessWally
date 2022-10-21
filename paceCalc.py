import os
import getch

# Prints pace calculator header message
def pace_header():

    clear = lambda: os.system('clear')
    clear()

    print("PACE CALCULATOR")

# Pace calculator main function
def pace_main():
    pace_header()

if __name__ == "__main__" :
    pace_main()