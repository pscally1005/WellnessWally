import os
import getch

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def bmi_infoPrint(unit=-1, height=-1, weight=-1):
    clear = lambda: os.system('clear')
    clear()

    print("BMI CALCULATOR")
    print("\nThis will allow you to enter your height and weight to calculate BMI")

    print("\nEnter \'1\' to use imperial units (in/lb)")
    print("Enter \'2\' to use metric units (cm/kg)")

    if unit == -1: return
    print(unit)

    if unit == "1":
        print("\nUsing imperial units (in/lb)")
    elif unit == "2":
        print("\nUsing metric units (cm/kg)")
    assert (unit == "1") or (unit == "2"), "ERROR: You entered: " + str(unit)

    print("\nPlease enter your height", end = " ")
    if unit == "1":
        print("(in)")
    else:
        print("(cm)")
    if height == -1: return
    if unit == "1":
        h = height / 0.0254
        print(h)
    else:
        h = height * 100
        print(h)

    print("\nPlease enter your weight", end = " ")
    if unit == "1":
        print("(lb)")
    else:
        print("(kg)")
    if weight == -1: return
    if unit == "1":
        w = weight / 0.45351473922
        print(w)
    else:
        w = weight
        print(w)

    bmi = weight / (height * height)
    bmi = round(bmi, 2)
    print("\nYour BMI is: " + str(bmi))

    if bmi < 18.5:
        print("You are in the UNDERWEIGHT weight range")
    elif bmi >- 18.5 and bmi < 25:
        print("You are in the NORMAL weight range")
    elif bmi >= 25 and bmi < 30:
        print("You are in the OVERWEIGHT weight range")
    else:
        print("You are in the OBESE weight range")

# User selects imperial or metric units for calculations
def bmi_unitSelect():
    bmi_infoPrint()
    unit = getch.getch()
    if unit == "1" or unit == "2":
        return unit
    return bmi_unitSelect()

# User inputs their height
# Converts the inputted height (in or cm) to m
def bmi_heightCalc(unit):

    bmi_infoPrint(unit)
    # User must input float height
    # Converts negative to positive if necessary
    height = input()
    if is_number(height) == False or float(height) <= 0:
        return bmi_heightCalc(unit)
    height = float(height)
        
    # If customary units, convert inches to meters
    if unit == "1":
        height = height * 0.0254

    # If metric units, convert centimeters to meters
    else:
        height = height / 100

    return height

# User inputs their weight
# Converts weight from lb to m, if necessary
def bmi_weightCalc(unit, height):

    bmi_infoPrint(unit, height)    
    # User must input float weight
    # Converts negative to positive if necessary
    weight = input()
    if is_number(weight) == False or float(weight) <= 0:
        return bmi_weightCalc(unit, height)
    weight = float(weight)
        
    # If customary units, convert inches to meters
    if unit == "1":
        weight = weight * 0.45351473922

    return weight 

# Gives user option to return to main menu or stay
def bmi_end(unit, height, weight):
    bmi_infoPrint(unit, height, weight)
    print("\nEnter \'Y\' to to stay on this screen, or anything else to return")
    exit = getch.getch()

    if exit == "Y" or exit == "y":
        return bmi_main()
    else:
        return

# BMI Calculator main function
def bmi_main():
    unit = bmi_unitSelect()
    height = bmi_heightCalc(unit)
    weight = bmi_weightCalc(unit, height)
    bmi_end(unit, height, weight)

if __name__ == "__main__" :
    bmi_main()