import os
import getch

# Prints BMI header message
def bmi_header():

    clear = lambda: os.system('clear')
    clear()

    print("BMI CALCULATOR")

# BMI Calculator main function
def bmi_main():
    bmi_header()

if __name__ == "__main__" :
    bmi_main()