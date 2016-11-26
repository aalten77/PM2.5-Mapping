import csv
from flask import Flask, render_template, redirect, url_for, request
from Site import Site
from collections import defaultdict
import datetime

app = Flask(__name__)

with open('daily_88101_2015.csv') as csvfile:
    reader = csv.DictReader(csvfile)

    Sites = []
    i = 0
    x = -1
    a = ''

    for row in reader:
        #if(i == 10):
        #    break;
        if (x != int(row['Site Num'])):
            Dictionary = defaultdict(dict)
            Site_Num = int(row['Site Num'])
            x = Site_Num
            Latitude = float(row['Latitude'])
            Longitude = float(row['Longitude'])
            s = Site(Site_Num, Latitude, Longitude)
            Sites.append(s)
            i = i + 1

        if (a != row['Date Local']):
            Day = row['Date Local']
            a = row['Date Local']
        if (row['AQI'] == ''):  # some of the values are negative which probably aren't real PM2.5 values. make 0
            Dictionary[Day] = -1;
        else:
            Dictionary[Day] = int(row['AQI'])
        Sites[i - 1].makeDict(Dictionary)
        #Sites[i - 1].makeJSON(Dictionary)

        #if (float(row['Sample Measurement']) < 0):  # some of the values are negative which probably aren't real PM2.5 values. make 0
        #    Sites[i - 1].add_GMTs_PM25s(row['Date GMT'], row['Time GMT'], 0.0)
        #   continue
        #Sites[i - 1].add_GMTs_PM25s(row['Date GMT'], row['Time GMT'], float(row['Sample Measurement']))
meow = 0

@app.route('/', methods = ['POST', 'GET'])
def display2016():
   startdate = request.form['startdate']
   enddate = request.form['enddate']
   print(startdate)
   print(enddate)
   for site in Sites:
       site.makeJSON(startdate, enddate)
   return render_template('map.html', Sites = Sites[0::10], startdate = startdate, enddate = enddate)

@app.route('/form')
def selectDays():
    return render_template('form.html')

@app.route('/map')
def displaymap():
    return render_template('map2.html')

if __name__ == '__main__':
   app.run(debug = True)