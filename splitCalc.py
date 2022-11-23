import os
import getch

# Prints split calculator header message
def split_header():

    clear = lambda: os.system('clear')
    clear()

    print("SPLIT CALCULATOR")

# Split calculator main function
def split_main():
    split_header()

if __name__ == "__main__" :
    split_main()