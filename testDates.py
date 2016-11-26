#!/usr/bin/env python
from datetime import datetime as dt, timedelta

def daterange( start_date, end_date ):
    if start_date <= end_date:
        for n in range( ( end_date - start_date ).days + 1 ):
            yield start_date + timedelta( n )
    else:
        for n in range( ( start_date - end_date ).days + 1 ):
            yield start_date - timedelta( n )

start = dt.strptime('01/01/2015 12:00 AM', '%m/%d/%Y %I:%M %p')
end = dt.strptime('02/01/2015 12:00 AM', '%m/%d/%Y %I:%M %p')
#start = datetime.date( year = 2010, month = 2, day = 1 )
#end = datetime.date( year = 2010, month = 1, day = 1 )

for date in daterange( start, end ):
    print (str(date.month) + '/' + str(date.day) + '/' + str(date.year))