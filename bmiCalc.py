import os
import getch

# Prints BMI header message
def bmi_header():

    clear = lambda: os.system('clear')
    clear()

    print("BMI CALCULATOR")
    print("\nThis will allow you to enter your height and weight to calculate BMI")

    print("\nEnter \'1\' to use imperial units (in/lb)")
    print("Enter \'2\' to use metric units (cm/kg)")

# User selects imperial or metric units for calculations
def bmi_unitSelect():
    unit = getch.getch()
    return unit

# Checks the users unit input
def bmi_checkUnit(unit):

    if unit == "\r" or unit == chr(27):
        print("\nYou entered: \'\'")
    else:
        print("\nYou entered: \'" + unit + "\'")

    if unit == "1":
        print("\nUsing imperial units (in/lb)")
        return unit
    elif unit == "2":
        print("\nUsing metric units (cm/kg)")
        return unit
    
    print("ERROR: Input is invalid.  Please try again")
    unit = getch.getch()
    bmi_header()
    bmi_checkUnit(unit)

# def bmi_heightImperial():

# def bmi_heightMetric():

# def bmi_weightImperial():

# def bmi_weightMetric():

# BMI Calculator main function
def bmi_main():
    bmi_header()
    unit = bmi_unitSelect()
    bmi_checkUnit(unit)

if __name__ == "__main__" :
    bmi_main()