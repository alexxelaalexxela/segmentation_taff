
from SatelliteData import SatelliteData
from os import listdir
from os.path import isdir, join
import math
import matplotlib.pyplot as plt
import numpy as np
import cmd
import outliers
import cmds

satellites = {}
names = {}
dataDir = "data"
namesFile = join(dataDir, "names.txt")
name_seperator = '_'

typesNames = {
    "i": "Inclination",
    "e": "Eccentricity",
    "a": "Semi major axis",
    "o": "RAAN",
    "arg": "Argument of Perigee",
    "tles": "TLEs of the satellite"
}


def prepare_data():
    
    folders = [f for f in listdir(dataDir) if isdir(join(dataDir ,f))]

    with open(namesFile) as f:
        lines = f.readlines()
        for line in lines:
            tokens = line.split("\t")
            names[tokens[0]] = tokens[1][:-1]

    for folder in folders:
        satellite = SatelliteData.importFromFolder(join(dataDir,folder), names)
        satellites[satellite.getCospar()] = satellite

    cmds.list_satellites(satellites)




class Request(cmd.Cmd):

    prompt = "Request > "

    def tokenize(self, tokens):
        return tokens.strip().split(" ")
    
    def checkArgs(self, tokens, bounds):
        nbTokens = len(tokens)
        if(nbTokens < bounds[0] or nbTokens > bounds[1]):
            if bounds[0] == bounds[1]:
                print("Invalid amount of arguments. Got {}, should be exactly {}".format(nbTokens, bounds[0]))
            else:
                print("Invalid amount of arguments. Got {}, should be between {} and {}".format(nbTokens, bounds[0], bounds[1]))
            return False
        return True

    def do_exit(self, line):
        print("Goodbye!")
        exit()

    def do_outliers(self, args):
        cospar = args
        cmds.tle_outliers(cospar, dataDir)

    def do_plot(self, args):
        minArgs = 2
        tokens = self.tokenize(args)
        nbTokens = len(tokens)
        if nbTokens < minArgs:
            
            return
        cmds.plot(tokens, satellites, typesNames, names)

    def do_list(self, _):
        cmds.list_satellites(satellites)

    def do_detectManoeuver(self, args):
        cospar = args
        cmds.maneuvers(cospar, dataDir)


    def do_cp(self, args):
        argsBounds = (3,3)
        tokens = self.tokenize(args)
        if not self.checkArgs(tokens, argsBounds):
            return
        
        cospar = tokens[0]
        type = tokens[1]
        doInterp = bool(int(tokens[2]))
        
        dates = satellites[cospar].getDates()
        ys = satellites[cospar].getData()[type]

        cmds.cp_detection(dates, ys, doInterp)

def main():
    prepare_data()
    Request().cmdloop()
    #run()
    #test()

if __name__ == "__main__":
    main()