import json
from datetime import datetime as dt, timedelta

class Site:

    def __init__(self, Site_Num, Latitude, Longitude):
        self.Site_Num = Site_Num
        self.Latitude = Latitude
        self.Longitude = Longitude
        self.Dictionary = {}
        self.DictJSON = {}
        #self.Date_GMTs = []
        #self.Time_GMTs = []
        #self.PM25s = []

    #def add_GMTs_PM25s(self, Date_GMT, Time_GMT, PM25):
    #    self.Date_GMTs.append(Date_GMT)
    #    self.Time_GMTs.append(Time_GMT)
    #    self.PM25s.append(PM25)

    def makeDict(self, Dictionary):
        self.Dictionary = Dictionary

    def daterange(start_date, end_date):
        if start_date <= end_date:
            for n in range((end_date - start_date).days + 1):
                yield start_date + timedelta(n)
        else:
            for n in range((start_date - end_date).days + 1):
                yield start_date - timedelta(n)

    def makeJSON(self, startdate, enddate):

        start = dt.strptime(startdate, '%m/%d/%Y %I:%M %p')
        end = dt.strptime(enddate, '%m/%d/%Y %I:%M %p')
        # start = datetime.date( year = 2010, month = 2, day = 1 )
        # end = datetime.date( year = 2010, month = 1, day = 1 )
        newDictionary = {}
        for date in Site.daterange(start, end):
            datestr = str(date.month) + '/' + str(date.day) + '/' + str(date.year)
            newDictionary[datestr] = self.Dictionary[datestr]
        self.DictJSON = json.dumps(newDictionary)