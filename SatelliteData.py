from os import listdir
from os.path import isfile, join
import math
import dateutil

name_separator = '_'
funs = {
    "i": lambda x : math.degrees(float(x)),
    "e": lambda x : float(x),
    "a": lambda x : float(x)/1000.0,
    "o": lambda x : math.degrees(float(x)),
    "arg" : lambda x : lambda x : math.degrees(float(x))
}


class SatelliteData:


    def __init__(self, dates, data, cospar, name):
        self.dates = dates
        self.data = data
        self.cospar = cospar
        self.name = name
        
    def getDates(self):
        return self.dates

    def getData(self):
        return self.data

    def getCospar(self):
        return self.cospar

    def getAvailableParameters(self):
        return [param for param in self.data.keys()]

    def importFromFolder(folderPath, names):
        files = [f for f in listdir(folderPath) if isfile(join(folderPath ,f))]
        dates = []
        cospar = ""
        data = {}

        for file in files:
            cospar = file[:file.index(name_separator)]
            type = file[file.index(name_separator)+1:file.index(".")]
            if type == "tles":
                continue
            dates, ys = SatelliteData.readFile(join(folderPath,file), funs[type])
            
            data[type] = ys

        satName = names[cospar]
        return SatelliteData(dates, data, cospar, satName)

    def readFile(str, parseY):
        with open(str) as f:
            lines = f.readlines()
            dates = []
            ys = []

            for line in lines:
                tokens = line.split('\t')
                date = dateutil.parser.isoparse(tokens[0])
                y = parseY(tokens[1])
                dates.append(date)
                ys.append(y)

        return dates, ys