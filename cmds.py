import matplotlib.pyplot as plt
from helpers import *
import outliers
from tletools import TLE
from os import listdir
from os.path import isdir, join

def plot(args, satellites, typesNames, names):
    cospar = args[0]
    types = args[1:]

    if(not cospar in satellites):
        print("Unknown COSPAR, use \"list\" to see all available satellites")
        return
    if(len(types) > 2):
        print("Can't plot more than two types at once")
        return
    
    data = satellites[cospar].getData()
    types = [type for type in types if type in data]
    if not len(types):
        print("Unknown type, Available types are:")
        for type in data:
            print("\t{} ({})".format(type, typesNames[type]))
        return
    
    plt.figure()
    plt.title("{}".format(names[cospar]))
    
    dates = satellites[cospar].getDates()
    ys1 = satellites[cospar].getData()[types[0]]
    if len(types) > 1:
        ys2 = satellites[cospar].getData()[types[1]]

    plt.plot(dates, ys1, label=typesNames[types[0]], color="blue")
    if(len(types) > 1):
        plt.twinx().plot(dates, ys2, label=typesNames[types[1]], color="red")
    
    plt.legend()
    plt.grid(visible=True)
    plt.show(block=False)

def tle_outliers(cospar, dataDir):
    fichiers = [f for f in listdir(dataDir) if isdir(join(dataDir, f))]
    possibilities = [s for s in fichiers if s[-1:]=='A']
    if (cospar not in possibilities):
        print("entrer un cospar valable")
        return
    tleFile = "{}/{}/{}_tles.txt".format(dataDir, cospar, cospar)

    tles_lines = outliers.parseTLEs_lines(tleFile)


    filtered = outliers.filter(tles_lines)
    unfiltered = [TLE.from_lines(*l) for l in tles_lines]

    len(unfiltered)

    print("diff", len(unfiltered), len(filtered))

    dates_unfiltered = [tle.epoch.datetime for tle in unfiltered]
    dates_filtered = [tle.epoch.datetime for tle in filtered]

    ys_unfiltered = [tle.inc for tle in unfiltered]
    mean = np.mean(ys_unfiltered)
    ys_filtered = [tle.inc for tle in filtered]

    plt.plot(dates_unfiltered, ys_unfiltered-mean, "-o")
    for date in dates_filtered : 
        plt.axvline(date, linewidth=2, linestyle='--', color='red')#(dates_filtered, ys_filtered, color="red")
    plt.grid(visible=True)
    plt.show(block=False)

def maneuvers(cospar, dataDir):
    tleFile = "{}/{}/{}_tles.txt".format(dataDir, cospar, cospar)

    tles_lines = outliers.parseTLEs_lines(tleFile)


    filtered = outliers.maneuver(tles_lines)
    unfiltered = [TLE.from_lines(*l) for l in tles_lines]

    #maneuvers = outliers.maneuver(filtered)

    len(unfiltered)

    print("diff", len(unfiltered), len(filtered))

    dates_unfiltered = [tle.epoch.datetime for tle in unfiltered]
    dates_filtered = [tle[0].epoch.datetime for tle in filtered]

    ys_unfiltered = [tle.inc for tle in unfiltered]
    ys_filtered = [(tle[1].inc-tle[0].inc) for tle in filtered]

    plt.plot(dates_unfiltered, ys_unfiltered, "-o")
    for date in dates_filtered : 
        plt.axvline(date, linewidth=2, linestyle='--', color='red')#(dates_filtered, ys_filtered, color="red")
    plt.grid(visible=True)
    plt.show(block=False)

def cp_detection(dates, ys, doInterpolate=False):
    if doInterpolate:
        dates, ys = interpolate(dates, ys)
    disc = slidingWindow(ys)
    cp_indices = thresholding(disc)

    cp_ys = [ys[i] for i in cp_indices]
    cp_dates = [dates[i] for i in cp_indices]

    plt.figure()
    plt.title("{}".format("Interpolated values" if doInterpolate else "Default values"))
    plt.plot(dates, ys)
    plt.scatter(cp_dates, cp_ys, color="red")
    plt.show(block=False)

    return cp_dates, cp_ys

def list_satellites(satellites):
    print("Available Satellites:")
    for cospar in satellites.keys():
        print("\t{} ({})".format(cospar, satellites[cospar].name))  