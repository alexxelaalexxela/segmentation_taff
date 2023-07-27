from tletools import TLE
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from datetime import datetime
import numpy as np
from math import floor, degrees

def yearDayFractionToDatetime(year, dayOfYear):
    dayWhole = floor(dayOfYear)
    dayFraction = dayOfYear - dayWhole
    hours = floor(dayFraction * 24)
    minutes = floor((dayFraction*24 - hours) * 60.0)
    seconds = (((dayFraction*24 - hours) * 60.0) - minutes) * 60

    str = "{} {} {} {} {:3f}".format(year, dayWhole, hours, minutes, seconds)

    date = datetime.strptime(str, "%Y %j %H %M %S.%f")
    return date

def getInclination(position, velocity):
    r = np.array(position)
    v = np.array(velocity)
    h = np.cross(r, v)
    inclination = np.arccos(h[2] / np.linalg.norm(h))  # In radians
    return degrees(inclination)

def filter(tles_lines):
    # Always keep the first TLE by default
    filtered = [TLE.from_lines(*(tles_lines[0]))]
    cursor = 0
    for i in range(2, len(tles_lines)-2):
        before = tles_lines[i-1-cursor]
        after = tles_lines[i+1]
        before2 = tles_lines[i-2-cursor]
        after2 = tles_lines[i+2]
        curr = tles_lines[i]
        cursor = 0
        corr = TLE.from_lines(*curr)

        targetDate = corr.epoch.datetime
        '''if (targetDate.year > 2019 and targetDate.month > 5 and targetDate.day > 13):
            print("yo")'''
        #inclCurr = curr.inc

        satellite = twoline2rv(curr[1], curr[2], wgs72) 
        position, velocity = satellite.propagate(targetDate.year, targetDate.month, targetDate.day, targetDate.hour, targetDate.minute, targetDate.second)
        inclCurr = getInclination(position, velocity)

        satellite = twoline2rv(before[1], before[2], wgs72)
        position, velocity = satellite.propagate(targetDate.year, targetDate.month, targetDate.day, targetDate.hour, targetDate.minute, targetDate.second)
        inclBefore = getInclination(position, velocity)

        satellite = twoline2rv(after[1], after[2], wgs72)
        position, velocity = satellite.propagate(targetDate.year, targetDate.month, targetDate.day, targetDate.hour, targetDate.minute, targetDate.second)
        inclAfter = getInclination(position, velocity)

        satellite = twoline2rv(before2[1], before2[2], wgs72)
        position, velocity = satellite.propagate(targetDate.year, targetDate.month, targetDate.day, targetDate.hour, targetDate.minute, targetDate.second)
        inclBefore2 = getInclination(position, velocity)

        satellite = twoline2rv(after2[1], after2[2], wgs72)
        position, velocity = satellite.propagate(targetDate.year, targetDate.month, targetDate.day, targetDate.hour, targetDate.minute, targetDate.second)
        inclAfter2 = getInclination(position, velocity)

        deltaTot = abs(inclAfter - inclBefore)
        deltaA = abs(inclAfter - inclCurr)
        deltaTot2 = abs(inclAfter2 - inclBefore2)
        deltaA2 = abs(inclAfter2 - inclCurr)
        deltaB = abs(inclBefore - inclCurr)
        deltaB2 = abs(inclBefore2 - inclCurr)
        if  (((2*deltaTot > deltaA) or (2*deltaTot > deltaB)) or (deltaA < 0.0001) or (deltaB<0.0001)):
            filtered.append(corr)
        else : 
            cursor = 1

    filtered.append(TLE.from_lines(*(tles_lines[-1])))
    return filtered

def maneuver(tles_lines):
    # Always keep the first TLE by default
    filtered = []
    cursor = 0
    for i in range(2, len(tles_lines)-2):
        before = tles_lines[i-1]
        after = tles_lines[i+1]
        before2 = tles_lines[i]
        after2 = tles_lines[i+2]
        curr = tles_lines[i]
        curr2 = tles_lines[i+1]
        corr = TLE.from_lines(*curr)
        corr2 = TLE.from_lines(*curr2)
        
        targetDate = corr.epoch.datetime
        targetDate2 = corr2.epoch.datetime
        if (targetDate.year > 2016 and targetDate.month > 8 and targetDate.day > 5):
            print("yo")
        #inclCurr = curr.inc

        satellite = twoline2rv(curr[1], curr[2], wgs72)
        position, velocity = satellite.propagate(targetDate.year, targetDate.month, targetDate.day, targetDate.hour, targetDate.minute, targetDate.second)
        inclCurr = getInclination(position, velocity)

        satellite = twoline2rv(before[1], before[2], wgs72)
        position, velocity = satellite.propagate(targetDate.year, targetDate.month, targetDate.day, targetDate.hour, targetDate.minute, targetDate.second)
        inclBefore = getInclination(position, velocity)

        satellite = twoline2rv(after[1], after[2], wgs72)
        position, velocity = satellite.propagate(targetDate.year, targetDate.month, targetDate.day, targetDate.hour, targetDate.minute, targetDate.second)
        inclAfter = getInclination(position, velocity)

        satellite = twoline2rv(before2[1], before2[2], wgs72)
        position, velocity = satellite.propagate(targetDate2.year, targetDate2.month, targetDate2.day, targetDate2.hour, targetDate2.minute, targetDate2.second)
        inclBefore2 = getInclination(position, velocity)

        satellite = twoline2rv(after2[1], after2[2], wgs72)
        position, velocity = satellite.propagate(targetDate2.year, targetDate2.month, targetDate2.day, targetDate2.hour, targetDate2.minute, targetDate2.second)
        inclAfter2 = getInclination(position, velocity)

        satellite = twoline2rv(curr2[1], curr2[2], wgs72)
        position, velocity = satellite.propagate(targetDate2.year, targetDate2.month, targetDate2.day, targetDate2.hour, targetDate2.minute, targetDate2.second)
        inclCurr2 = getInclination(position, velocity)

        deltaTot = abs(inclAfter - inclBefore)
        deltaA = abs(inclAfter - inclCurr)
        deltaB = abs(inclBefore - inclCurr)

        deltaTot2 = abs(inclAfter2 - inclBefore2)
        deltaA2 = abs(inclAfter2 - inclCurr2)
        deltaB2 = abs(inclBefore2 - inclCurr2)
        if(deltaTot != 0 and (deltaB/deltaTot < 0.1 or deltaA/deltaTot < 0.1) and deltaB != 0 and deltaTot > 0.0025):
            if((deltaTot2 != 0 and (deltaB2/deltaTot2 < 0.1 or deltaA2/deltaTot2 < 0.1) and deltaB2 != 0 and deltaTot2 > 0.0025)): 
                filtered.append([corr, corr2])
             

    return filtered

def maneuver_errors(tles_lines):
    # Always keep the first TLE by default
    filtered = []
    cursor = 0
    mean_errors = []
    for i in range(1, len(tles_lines)-1):
        before = tles_lines[i-1]
        curr = tles_lines[i]
        corr = TLE.from_lines(*curr)

        targetDate = corr.epoch.datetime

        '''if (targetDate.year > 2016 and targetDate.month > 8 and targetDate.day > 5):
            print("yo")'''
        #inclCurr = curr.inc

        satellite = twoline2rv(curr[1], curr[2], wgs72)
        position, velocity = satellite.propagate(targetDate.year, targetDate.month, targetDate.day, targetDate.hour, targetDate.minute, targetDate.second)
        inclCurr = getInclination(position, velocity)

        satellite = twoline2rv(before[1], before[2], wgs72)
        position, velocity = satellite.propagate(targetDate.year, targetDate.month, targetDate.day, targetDate.hour, targetDate.minute, targetDate.second)
        inclBefore = getInclination(position, velocity)

        deltaError = abs(inclBefore/inclCurr)
        mean_errors.append(deltaError)
       

    mean_err = np.mean(mean_errors) 
    mean_standar = []    
    for i in range(1, len(tles_lines)-1):
        before = tles_lines[i-1]
        curr = tles_lines[i]
        corr = TLE.from_lines(*curr)

        targetDate = corr.epoch.datetime

        '''if (targetDate.year > 2016 and targetDate.month > 8 and targetDate.day > 5):
            print("yo")'''
        #inclCurr = curr.inc

        satellite = twoline2rv(curr[1], curr[2], wgs72)
        position, velocity = satellite.propagate(targetDate.year, targetDate.month, targetDate.day, targetDate.hour, targetDate.minute, targetDate.second)
        inclCurr = getInclination(position, velocity)

        satellite = twoline2rv(before[1], before[2], wgs72)
        position, velocity = satellite.propagate(targetDate.year, targetDate.month, targetDate.day, targetDate.hour, targetDate.minute, targetDate.second)
        inclBefore = getInclination(position, velocity)

        deltaError = abs(inclBefore/inclCurr)
        mean_standar.append(abs(mean_err-deltaError))

    mean_std = np.mean(mean_standar)

    for i in range(1, len(tles_lines)-1):
        before = tles_lines[i-1]
        curr = tles_lines[i]
        corr = TLE.from_lines(*curr)

        targetDate = corr.epoch.datetime

        '''if (targetDate.year > 2016 and targetDate.month > 8 and targetDate.day > 5):
            print("yo")'''
        #inclCurr = curr.inc

        satellite = twoline2rv(curr[1], curr[2], wgs72)
        position, velocity = satellite.propagate(targetDate.year, targetDate.month, targetDate.day, targetDate.hour, targetDate.minute, targetDate.second)
        inclCurr = getInclination(position, velocity)

        satellite = twoline2rv(before[1], before[2], wgs72)
        position, velocity = satellite.propagate(targetDate.year, targetDate.month, targetDate.day, targetDate.hour, targetDate.minute, targetDate.second)
        inclBefore = getInclination(position, velocity)

        deltaError = abs(inclBefore/inclCurr)
        mean_standar.append(abs(mean_err-deltaError))
        if(abs(deltaError-mean_err) > 10*mean_std): 
            filtered.append(corr)
        '''if(deltaError > 1.5*mean_err):
            filtered.append(corr)'''
             
    return filtered


def parseTLEs_lines(file):
    tles_lines = []
    with open(file) as f:
        lines = f.readlines()
        for i in range(0, len(lines), 3):
            tle_lines = [lines[i], lines[i+1], lines[i+2]]
            tles_lines.append(tle_lines)
    return tles_lines