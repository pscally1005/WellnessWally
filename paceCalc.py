import os
import getch

# Console line printing
def infoPrint(unit=-1, select=-1, dist=-1, time=-1, pace=-1):
    clear = lambda: os.system('clear')
    clear()

    print("PACE CALCULATOR")
    print("This will allow you to calculate pace, distance, or time")

    print("\nEnter \'1\' to use imperial units (mi)")
    print("Enter \'2\' to use metric units (km)")

    if unit == -1:
        return
    print(unit)

    if unit == "1":
        print("\nUsing imperial units (mi)")
    elif unit == "2":
        print("\nUsing metric units (km)")
    assert (unit == "1") or (unit == "2"), "ERROR: You entered: " + str(unit)

    print("\nWhat would you like to calculate?")
    print("D: Distance")
    print("T: Time")
    print("P: Pace")
    print("\nPlease enter a letter to select")

    if select == -1:
        return
    print(select)

    if select == "d" or select == "D":
        print("\nCalculating distance...")
    elif select == "t" or select == "T":
        print("\nCalculating time...")
    elif select == "p" or select == "P":
        print("\nCalculating pace...")
    assert select == "d" or select == "D" or select == "t" or select == "T" or select == "p" or select == "P"

    print("\nEnter a distance in", end = " ")
    if unit == "1":
        print("miles")
    else:
        print("kilometers")

    if dist == -1:
        return
    print(dist)

    print("\nEnter a time (Format: HH:MM:SS)")

    if time == -1:
        return
    print(time)

    print("\nEnter a pace in", end = " ")
    if unit == "1":
        print("min/mi", end = " ")
    else:
        print("min/km", end = " ")
    print("(Format: MM:SS)")

    if pace == -1:
        return
    print(pace)

    print()
    if dist != "X":
        print("You entered a distance of: " + str(dist), end = " ")
        if unit == "1" : print("[mi]")
        else : print("[km]")

    if time != "X":
        print("You entered a time of: " + time)

    if pace != "X":
        print("You entered a pace of: " + pace, end = " ")
        if unit == "1" : print("[min/mi]")
        else : print("[min/km]")
    print()

# Checks the users unit input
def pace_unitInput():
    infoPrint()
    unit = getch.getch()
    if unit == "1" or unit == "2":
        return unit
    return pace_unitInput()

# Checks user calc selection input
def pace_selectInput(unit):
    infoPrint(unit)
    select = getch.getch()
    if select == "D" or select == 'd' or select == "T" or select == "t" or select == "P" or select == "p":
        return select
    return pace_selectInput(unit)

# User input for distance
def pace_distanceInput(unit, select):
    infoPrint(unit, select)
    if select == "d" or select == "D":
        return "X"

    # User must input float distance
    dist = input()
    try:
        dist = float(dist)
        if dist < 0:
            dist = dist * -1
    except:
        return pace_distanceInput(unit, select)
    return dist

# User input for time
def pace_timeInput(unit, select, dist):
    infoPrint(unit, select, dist)
    if select == "t" or select == "T":
        return "X"

    # User must input time in format HH:MM:SS
    time = input()
    if len(time) != 8 or time[2] != ":" or time[5] != ":":
        return pace_timeInput(unit, select, dist)

    try:
        timeHour, timeMin, timeSec = time.split(":")
        assert len(timeHour) == 2 and len(timeMin) == 2 and len(timeSec) == 2

        float(timeHour[0])
        float(timeHour[1])
        float(timeMin[0])
        float(timeMin[1])
        float(timeSec[0])
        float(timeSec[1])

        timeHour = int(timeHour)
        timeMin = int(timeMin)
        timeSec = int(timeSec)

        if timeSec >= 60:
            timeSec = "a"
            int(timeSec)

        if int(timeMin) >= 60:
            timeMin = "a"
            int(timeMin)

    except:
        return pace_timeInput(unit, select, dist)
  
    return time

# User input for pace
def pace_paceInput(unit, select, dist, time):
    infoPrint(unit, select, dist, time)
    if select == "p" or select == "P":
        return "X"

    # User must input pace in format MM:SS
    pace = input()
    if len(pace) != 5 or pace[2] != ":":
        return pace_paceInput(unit, select, dist, time)

    try:
        paceMin, paceSec = pace.split(":")
        assert len(paceMin) == 2 and len(paceSec) == 2

        int(paceMin[0])
        int(paceMin[1])
        int(paceSec[0])
        int(paceSec[1])

        paceMin = int(paceMin)
        paceSec = int(paceSec)

        if paceSec >= 60:
            paceSec = "a"
            int(paceSec)
    except:
        return pace_paceInput(unit, select, dist, time)
  
    return pace   

#TODO: actual dist/time/pace calculations
def pace_distCalc(unit, select, dist, pace, time):
    assert(dist == "X")

    print("Calculated distance: " + dist)
    return dist

def pace_timeCalc(unit, select, dist, time, pace):
    assert(time == "X")

    print("Calculated time: " + time)
    return time

def pace_paceCalc(unit, select, dist, time, pace):
    assert(pace == "X")

    print("Calculated pace: " + pace)
    return pace


# Pace calculator main function
def pace_main():
    unit = pace_unitInput()
    select = pace_selectInput(unit)
    dist = pace_distanceInput(unit, select)
    time = pace_timeInput(unit, select, dist)
    pace = pace_paceInput(unit, select, dist, time)

    infoPrint(unit, select, dist, time, pace)
    if dist == "X":
        pace_distCalc(unit, select, dist, time, pace)
    elif time == "X":
        pace_timeCalc(unit, select, dist, time, pace)
    elif pace == "X":
        pace_paceCalc(unit, select, dist, time, pace)
    else:
        print("ERROR")

if __name__ == "__main__" :
    pace_main()