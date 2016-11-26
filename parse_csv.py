import csv
from Site import Site
from collections import defaultdict
import json
with open('hourly_88101_2016/hourly_88101_2016.csv') as csvfile:
    reader = csv.DictReader(csvfile)

    Sites = []
    i = 0
    x = -1
    a = ''

    for row in reader:
        if (x != int(row['Site Num'])):
            Dictionary = defaultdict(dict)
            Site_Num = int(row['Site Num'])
            x = Site_Num
            Latitude = float(row['Latitude'])
            Longitude = float(row['Longitude'])
            s = Site(Site_Num, Latitude, Longitude)
            Sites.append(s)
            i = i + 1

        if (a != row['Date GMT']):
            Day = row['Date GMT']
            a = row['Date GMT']
        Dictionary[Day][row['Time GMT']] = float(row['Sample Measurement'])
        Sites[i-1].makeDict(Dictionary)
        Sites[i-1].makeJSON(Dictionary)

    #json_data = json.dumps(Sites[0].Dictionary)
       #if(float(row['Sample Measurement']) < 0): #some of the values are negative which probably aren't real PM2.5 values. make 0
       #     Sites[i - 1].add_GMTs_PM25s(row['Date GMT'], row['Time GMT'], 0.0)
       #     continue
        #Sites[i-1].add_GMTs_PM25s(row['Date GMT'], row['Time GMT'], float(row['Sample Measurement']))
    meow = 0