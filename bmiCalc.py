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
    return bmi_checkUnit(unit)

# Clears screen, reprints info up until height
def bmi_clearForHeight(unit):

    bmi_header()
    print("\nYou entered: \'" + unit + "\'")
    if unit == "1":
        print("\nUsing imperial units (in/lb)")
    elif unit == "2":
        print("\nUsing metric units (cm/kg)")

# User inputs their height
# Converts the inputted height (in or cm) to m
def bmi_heightCalc(unit):

    bmi_clearForHeight(unit)
    assert (unit == "1") or (unit == "2"), "ERROR: You entered: " + str(unit)
    print("\nPlease enter your height", end = " ")
    if unit == "1":
        print("(in)")
    else:
        print("(cm)")

    # User must input float height
    # Converts negative to positive if necessary
    height = input()
    try:
        height = float(height)
        if height < 0:
            height = height * -1
    except:
        bmi_header()
        return bmi_heightCalc(unit)
        
    # If customary units, convert inches to meters
    if unit == "1":
        height = height * 0.0254

    # If metric units, convert centimeters to meters
    else:
        height = height / 100

    return height

# Clears screen, reprints info up until weight
def bmi_clearForWeight(unit, height):

    bmi_clearForHeight(unit)
    print("\nPlease enter your height", end = " ")
    if unit == "1":
        print("(in)")
    else:
        print("(cm)")
    if unit == "1":
        print(str(round(height / 0.0254, 2)))
    else:
        print(str(round(height * 100, 2)))

# User inputs their weight
# Converts weight from lb to m, if necessary
def bmi_weightCalc(unit, height):

    bmi_clearForWeight(unit, height)    
    assert (unit == "1") or (unit == "2"), "ERROR: You entered: " + str(unit)
    print("\nPlease enter your weight", end = " ")
    if unit == "1":
        print("(lb)")
    else:
        print("(kg)")

    # User must input float weight
    # Converts negative to positive if necessary
    weight = input()
    try:
        weight = float(weight)
        if weight < 0:
            weight = weight * -1
    except:
        bmi_header()
        return bmi_weightCalc(unit, height)
        
    # If customary units, convert inches to meters
    if unit == "1":
        weight = weight * 0.45351473922

    return weight

# Clears screen, reprints info up until BMI calculation
def bmi_clearForCalc(unit, height, weight):

    bmi_clearForWeight(unit, height)
    print("\nPlease enter your weight", end = " ")
    if unit == "1":
        print("(lb)")
    else:
        print("(kg)")
    if unit == "1":
        print(str(round(weight / 0.45351473922, 2)))
    else:
        print(str(round(weight, 2)))

# Calculates the users BMI, gives weight ranges
def bmi_calc(height, weight):

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

# Gives user option to return to main menu or stay
def bmi_end():

    print("\nEnter \'Y\' to to stay on this screen, or anything else to return")
    exit = getch.getch()

    if exit == "Y" or exit == "y":
        return bmi_main()
    else:
        return

# BMI Calculator main function
def bmi_main():
    bmi_header()
    unit = bmi_unitSelect()
    unit = bmi_checkUnit(unit)
    height = bmi_heightCalc(unit)
    weight = bmi_weightCalc(unit, height)
    bmi_clearForCalc(unit, height, weight)
    bmi_calc(height, weight)
    bmi_end()

if __name__ == "__main__" :
    bmi_main()