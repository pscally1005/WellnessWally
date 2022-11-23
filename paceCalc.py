import os
import getch
import datetime

# Console line printing
def pace_infoPrint(unit=-1, select=-1, dist=-1, time=-1, pace=-1):
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
        if unit == "1" : 
            print("mi", end = " ")
            d_km = dist * 1.60934
            d_km = str(round(d_km, 2))
            print("(" + d_km + " km)")
        else : 
            print("km", end = " ")
            d_mi = dist / 1.60934
            d_mi = str(round(d_mi, 2))
            print("(" + d_mi + " mi)")

    if time != "X":
        print("You entered a time of: " + time)

    if pace != "X":
        p_sec = pace_convPace(pace)
        print("You entered a pace of: " + pace, end = " ")
        if unit == "1" :
            print("min/mi", end = " ")
            p_minkm = p_sec / 1.60934
            #p_minkm is the min per km (pace), but as a decimal.  conv to proper format
            p_minkm = str(datetime.timedelta(seconds=p_minkm))
            p_minkm = p_minkm[3:7]
            print("(" + p_minkm + " min/km)")
        else : 
            print("min/km", end = " ")
            p_minmi = p_sec * 1.60934
            #p_minmi is the min per km (pace), but as a decimal.  conv to proper format
            p_minmi = str(datetime.timedelta(seconds=p_minmi))
            p_minmi = p_minmi[3:7]
            print("(" + p_minmi + " min/mi)")
    print()

# Checks the users unit input
def pace_unitInput():
    pace_infoPrint()
    unit = getch.getch()
    if unit == "1" or unit == "2":
        return unit
    return pace_unitInput()

# Checks user calc selection input
def pace_selectInput(unit):
    pace_infoPrint(unit)
    select = getch.getch()
    if select == "D" or select == 'd' or select == "T" or select == "t" or select == "P" or select == "p":
        return select
    return pace_selectInput(unit)

# User input for distance
def pace_distanceInput(unit, select):
    pace_infoPrint(unit, select)
    if select == "d" or select == "D":
        return "X"

    # User must input float distance
    dist = input()
    try:
        dist = float(dist)
        if dist < 0:
            dist = dist * -1

        if dist == 0:
            dist = "a"
            int(dist)
    except:
        return pace_distanceInput(unit, select)
    return dist

# User input for time
def pace_timeInput(unit, select, dist):
    pace_infoPrint(unit, select, dist)
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

        t = pace_convTime(time)
        if t <= 0:
            t = "a"
            int(t)

    except:
        return pace_timeInput(unit, select, dist)
  
    return time

# User input for pace
def pace_paceInput(unit, select, dist, time):
    pace_infoPrint(unit, select, dist, time)
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

        p = pace_convPace(pace)
        if p <= 0:
            p = "a"
            int(p)
    except:
        return pace_paceInput(unit, select, dist, time)
  
    return pace   

# Converts the time string into seoonds
def pace_convTime(time):
    # convert time into seconds
    assert len(time) == 8
    timeHour = int( str(time[0]) + str(time[1]) )
    timeMin = int( str(time[3]) + str(time[4]) )
    timeSec = int( str(time[6]) + str(time[7]) )

    seconds = timeSec + (timeMin*60) + (timeHour*60*60)
    return seconds

# Converts the pace string into seconds
def pace_convPace(pace):
    # convert time into seconds
    assert len(pace) == 5
    paceMin = int( str(pace[0]) + str(pace[1]) )
    paceSec = int( str(pace[3]) + str(pace[4]) )
    
    seconds = paceSec + (paceMin*60)
    return seconds

# Given a time and a pace, caculate distance
def pace_distCalc(unit, select, dist, time, pace):
    assert(dist == "X")

    t = pace_convTime(time)
    p = pace_convPace(pace)
    d = float(t) / float(p)
    d = float(str(round(d, 2)))

    print("Calculated distance: " + str(d), end = " ")
    assert unit == "1" or unit == "2"
    if unit == "1":
        print("mi", end = " ")
        d_km = d * 1.60934
        d_km = str(round(d_km, 2))
        print("(" + d_km + " km)")
    elif unit == "2":
        print("km", end = " ")
        d_mi = d / 1.60934
        d_mi = str(round(d_mi, 2))
        print("(" + d_mi + " mi)")

# Given a distance and a pace, calculate time
def pace_timeCalc(unit, select, dist, time, pace):
    assert(time == "X")

    d = dist
    p = pace_convPace(pace)
    t = float( float(d) * float(p)) + 10**-4

    # convert time in seconds back to string
    t = str(datetime.timedelta(seconds=t))

    print("Calculated time: " + str(t[0:10]))

# Given a distance and a time, calculate pace
def pace_paceCalc(unit, select, dist, time, pace):
    assert(pace == "X")

    d = dist
    t = pace_convTime(time)
    p_sec = float( float(t) / float(d) ) + 10**-4

    # convert pace in seconds back to string
    p = str(datetime.timedelta(seconds=p_sec))
    l = len(p)
    p = p[3:l]

    print("Calculated pace: " + p[0:7], end = " ")
    assert unit == "1" or unit == "2"
    if unit == "1":
        print("min/mi", end = " ")
        p_minkm = p_sec / 1.60934
        #p_minkm is the min per km (pace), but as a decimal.  conv to proper format
        p_minkm = str(datetime.timedelta(seconds=p_minkm))
        p_minkm = p_minkm[3:l]
        print("(" + p_minkm[0:7] + " min/km)")
    elif unit == "2":
        print("min/km", end = " ")
        p_minmi = p_sec * 1.60934
        #p_minmi is the min per mi (pace), but as a decimal.  conv to proper format
        p_minmi = str(datetime.timedelta(seconds=p_minmi))
        p_minmi = p_minmi[3:l]
        print("(" + p_minmi[0:7] + " min/mi)")

# Gives user option to return to main menu or stay
def pace_end():
    print("\nEnter \'Y\' to to stay on this screen, or anything else to return")
    exit = getch.getch()

    if exit == "Y" or exit == "y":
        return pace_main()
    else:
        return

# Pace calculator main function
def pace_main():
    unit = pace_unitInput()
    select = pace_selectInput(unit)
    dist = pace_distanceInput(unit, select)
    time = pace_timeInput(unit, select, dist)
    pace = pace_paceInput(unit, select, dist, time)

    pace_infoPrint(unit, select, dist, time, pace)
    if dist == "X":
        pace_distCalc(unit, select, dist, time, pace)
    elif time == "X":
        pace_timeCalc(unit, select, dist, time, pace)
    elif pace == "X":
        pace_paceCalc(unit, select, dist, time, pace)
    else:
        print("ERROR")
    pace_end()

if __name__ == "__main__" :
    pace_main()