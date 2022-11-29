import os
import getch
import datetime
from paceCalc import *

# Console line printing for splitCalc.py
def split_infoPrint(unit=-1, pace=-1):
    clear = lambda: os.system('clear')
    clear()
    print("SPLIT CALCULATOR")
    print("This will allow you to input a pace and find out your splits")

    print("\nEnter \'1\' to use imperial units (min/mi)")
    print("Enter \'2\' to use metric units (min/km)")

    if unit == -1: return
    print(unit)

    assert (unit == "1") or (unit == "2"), "ERROR: You entered: " + str(unit)
    if unit == "1": print("\nUsing imperial units (min/mi)")
    else:   print("\nUsing metric units (min/km)")

    print("\nEnter a pace in", end = " ")
    if unit == "1": print("min/mi", end = " ")
    else: print("min/km", end = " ")
    print("(Format: MM:SS)")

    if pace == -1: return
    print(pace)

    s = pace_convPace(pace)
    paceLead0 = str(datetime.timedelta(seconds=s))
    # print(paceLead0)
    print("\nYou entered a pace of: " + paceLead0, end = " ")
    p_sec = pace_convPace(pace)
    p = pace_paceSwitchUnits(unit, p_sec)
    if unit == "1": print("\mi (" + p + " \km )")
    else: print("/km (" + p + " /mi )")

# User selects imperial or metric units for calculations
def split_unitSelect():
    split_infoPrint()
    unit = getch.getch()
    if unit == "1" or unit == "2":
        return unit
    return split_unitSelect()

# User input for pace
def split_paceInput(unit):
    split_infoPrint(unit)

    # User must input pace in format MM:SS
    pace = input()
    if len(pace) != 5 or pace[2] != ":":
        return split_paceInput(unit)

    try:
        paceMin, paceSec = pace.split(":")
        assert len(paceMin) == 2 and len(paceSec) == 2

        int(paceMin[0])
        int(paceMin[1])
        int(paceSec[0])
        int(paceSec[1])

        paceMin = int(paceMin)
        paceSec = int(paceSec)

        p = pace_convPace(pace)
        if paceSec >= 60 or p <= 0:
            paceSec = "a"
            int(paceSec)

    except:
        return split_paceInput(unit)
  
    return pace  

def split_calculator(unit, pace):
    split_infoPrint(unit,pace)

    [pace_mi, pace_km] = [-1, -1]
    assert unit == "1" or unit == "2"
    p = pace_convPace(pace)
    if unit == "1":
        assert len(pace) == 5
        m, s = pace.split(":")
        pace_mi = float( int(m)*60 + int(s) )

        pace_km = pace_paceSwitchUnits(unit,p)
        assert len(pace_km) == 10 or len(pace_km) == 11
        h, m, s, = pace_km.split(":")
        s, d = s.split(".")
        pace_km = float( int(h)*3600 + int(m)*60 + int(s) + int(d)/100 )


    else:
        pace_mi = pace_paceSwitchUnits(unit,p)
        assert len(pace_mi) == 10 or len(pace_mi) == 11
        h, m, s, = pace_mi.split(":")
        s, d = s.split(".")
        pace_mi = float( int(h)*3600 + int(m)*60 + int(s) + int(d)/100 )

        assert len(pace) == 5
        m, s = pace.split(":")
        pace_km = float( int(m)*60 + int(s) )

    # print(str(pace_mi) + " " + str(pace_km))
    split_100 = str(datetime.timedelta(seconds=pace_km * 0.1 + 10**-6))[0:-4]
    split_200 = str(datetime.timedelta(seconds=pace_km * 0.2 + 10**-6))[0:-4]
    split_400 = str(datetime.timedelta(seconds=pace_km * 0.4 + 10**-6))[0:-4]
    split_800 = str(datetime.timedelta(seconds=pace_km * 0.8 + 10**-6))[0:-4]
    split_1k  = str(datetime.timedelta(seconds=pace_km * 1.0 + 10**-6))[0:-4]
    split_16  = str(datetime.timedelta(seconds=pace_km * 1.6 + 10**-6))[0:-4]
    split_1mi = str(datetime.timedelta(seconds=pace_mi * 1.0 + 10**-6))[0:-4]
    split_5k  = str(datetime.timedelta(seconds=pace_km * 5.0 + 10**-6))[0:-4]
    split_10k = str(datetime.timedelta(seconds=pace_km * 10  + 10**-6))[0:-4]
    split_half= str(datetime.timedelta(seconds=pace_mi *13.1 + 10**-6))[0:-4]
    split_full= str(datetime.timedelta(seconds=pace_mi *26.2 + 10**-6))[0:-4]
    
    print("100 m:\t\t" + split_100)
    print("200 m:\t\t" + split_200)
    print("400 m:\t\t" + split_400)
    print("800 m:\t\t" + split_800)
    print("1 km: \t\t" + split_1k)
    print("1.6 km: \t" + split_16)
    print("1 mi: \t\t" + split_1mi)
    print("5 km: \t\t" + split_5k)
    print("10 km:\t\t" + split_10k)
    print("13.1 mi:\t" + split_half)
    print("26.2 mi:\t" + split_full)

# Gives user option to return to main menu or stay
def split_end():
    print("\nEnter \'Y\' to to stay on this screen, or anything else to return")
    exit = getch.getch()

    if exit == "Y" or exit == "y":
        return split_main()
    else:
        return

# Split calculator main function
def split_main():
    unit = split_unitSelect()
    pace = split_paceInput(unit)
    split_calculator(unit, pace)
    split_end()

if __name__ == "__main__" :
    split_main()