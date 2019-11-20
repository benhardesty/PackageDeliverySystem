"""Module containing utility functions."""

import math

def convert_standard_time_to_minutes(time):
    """
    Convert a time stamp in standard time to minutes.

    Keyword arguments:
    time -- a string in the format of HH:MM:SS AM/PM (E.g. 10:00:00 AM).
    """

    if time == "EOD":
        time = "05:00:00 PM"
    hour = int(time.split(" ")[0].split(":")[0]) % 12 * 60
    minute = int(time.split(" ")[0].split(":")[1])
    AMPM = 0 if time.split(" ")[1] == "AM" else 12 * 60
    return hour + minute + AMPM

def convert_minutes_to_standard_time(time):
    """
    Convert a time stamp in minutes to standard time (E.g. 10:00:00 AM).

    Keyword arguments:
    time -- time in minutes from the start of the day.
    """

    hours = math.floor(int(time)/60)
    AMPM = "AM" if hours < 12 else "PM"
    if hours > 12:
        hours = hours % 12
    if hours < 10:
        hours = "0" + str(hours)
    else:
        hours = str(hours)
    minutes = int(time) % 60
    minutes = str(minutes) if minutes >= 10 else "0" + str(minutes)
    return str(hours) + ":" + str(minutes) + ":00 " + AMPM
