import os
import getch

# Prints pace calculator header message
def pace_header():

    clear = lambda: os.system('clear')
    clear()

    print("PACE CALCULATOR")
    print("This will allow you to calculate pace, distance, or time")

    print("\nEnter \'1\' to use imperial units (in/lb)")
    print("Enter \'2\' to use metric units (cm/kg)")

# User selects imperial or metric units for calculations
def pace_unitSelect():
    unit = getch.getch()
    return unit

# Checks the users unit input
def pace_checkUnit(unit):

    if unit == "\r" or unit == "\n" or unit == chr(27):
        print("\nYou entered: \'\'")
    else:
        print("\nYou entered: \'" + unit + "\'")

    if unit == "1":
        print("\nUsing imperial units (mi)")
        return unit
    elif unit == "2":
        print("\nUsing metric units (km)")
        return unit
    
    print("ERROR: Input is invalid.  Please try again")
    unit = getch.getch()
    pace_header()
    return pace_checkUnit(unit)

# Clears screen, reprints info up until distance input
def pace_clearForDistance(unit):
    pace_header()
    assert (unit == "1") or (unit == "2"), "ERROR: You entered: " + str(unit)
    print("\nYou entered: \'" + unit + "\'")
    if unit == "1":
        print("\nUsing imperial units (mi)")
    else:
        print("\nUsing metric units (km)")

# User input for distance
def pace_inputDistance(unit):

    pace_clearForDistance(unit)
    print("\nEnter a distance in", end = " ")
    if unit == "1":
        print("miles")
    else:
        print("kilometers")

    # User must input float distance
    dist = input()
    try:
        for i in range(0, len(dist)):
            float(str(dist)[i])
        dist = float(dist)
    except:
        return pace_inputDistance(unit)
  
    return dist

# Clears screen, reprints info up until time input
def pace_clearForTime(unit, dist):
    pace_clearForDistance(unit,)
    assert (unit == "1") or (unit == "2"), "ERROR: You entered: " + str(unit)
    print("\nEnter a distance in", end = " ")
    if unit == "1":
        print("miles")
    else:
        print("kilometers")
    print(dist)

# User input for time
def pace_inputTime(unit, dist):
    pace_clearForTime(unit, dist)
    print("\nEnter a time (Format: HH:MM:SS)")

    # User must input time in format HH:MM:SS
    time = input()
    if len(time) != 8 or time[2] != ":" or time[5] != ":":
        return pace_inputTime(unit, dist)

    try:
        timeHour, timeMin, timeSec = time.split(":")
        assert len(timeHour) == 2 and len(timeMin) == 2 and len(timeSec) == 2

        float(timeHour[0])
        float(timeHour[1])
        float(timeMin[0])
        float(timeMin[1])
        float(timeSec[0])
        float(timeSec[1])

        timeHour = float(timeHour)
        timeeMin = float(timeMin)
        timeSec = float(timeSec)
    except:
        return pace_inputTime(unit, dist)
  
    return time

# Clears screen, reprints info up until pace input
def pace_clearForPace(unit, dist, time):
    pace_clearForTime(unit, dist)
    assert (unit == "1") or (unit == "2"), "ERROR: You entered: " + str(unit)
    print("\nEnter a time (Format: HH:MM:SS)")
    print(time)

# User input for pace
def pace_inputPace(unit, dist, time):
    pace_clearForPace(unit, dist, time)
    print("\nEnter a pace in", end = " ")
    if unit == "1":
        print("min/mi", end = " ")
    else:
        print("min/km", end = " ")
    print("(Format: MM:SS)")

    # User must input pace in format MM:SS
    pace = input()
    if len(pace) != 5 or pace[2] != ":":
        return pace_inputPace(unit, dist, time)

    try:
        paceMin, paceSec = pace.split(":")
        assert len(paceMin) == 2 and len(paceSec) == 2

        float(paceMin[0])
        float(paceMin[1])
        float(paceSec[0])
        float(paceSec[1])

        paceMin = float(paceMin)
        paceSec = float(paceSec)
    except:
        return pace_inputPace(unit, dist, time)
  
    return pace   

# Prints the user inputs before calculations
def pace_printInputs(unit, dist, time, pace):
    pace_clearForPace(unit, dist, time)
    print("\nEnter a pace in", end = " ")
    if unit == "1":
        print("min/mi", end = " ")
    else:
        print("min/km", end = " ")
    print("(Format: MM:SS)")
    print(pace)

    print("\nYou entered a distance of: " + str(dist), end = " ")
    if unit == "1" : print("[mi]")
    else : print("[km]")

    print("You entered a time of: " + time)

    print("You entered a pace of: " + pace, end = " ")
    if unit == "1" : print("[min/mi]")
    else : print("[min/km]")

#TODO: paceSec and timeSec cant be >= 60
#TODO: timeMin cant be >= 60, but paceMin can be
#TODO: have user select which one they would like to calculate (either the x method or at start)
#TODO: actual dist/time/pace calculations

# Pace calculator main function
def pace_main():
    pace_header()
    unit = pace_unitSelect()
    unit = pace_checkUnit(unit)
    dist = pace_inputDistance(unit)
    time = pace_inputTime(unit, dist)
    pace = pace_inputPace(unit, dist, time)
    pace_printInputs(unit, dist, time, pace)

if __name__ == "__main__" :
    pace_main()