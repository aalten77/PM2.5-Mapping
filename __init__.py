import csv
import json
from flask import Flask, render_template, redirect, url_for, request
from Site import Site
from collections import defaultdict
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['LOAD_FROM_CSV'] = False
app.config['DATE_FORMAT'] = '%m/%d/%Y'

db = SQLAlchemy(app)


class Site(db.Model):
    __tablename__ = "sites"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    site_num = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    date = db.Column(db.DateTime)
    aqi = db.Column(db.Integer)

    def __init__(self, site_num, lat, lng, date, aqi):
        self.site_num = site_num
        self.lat = lat
        self.lng = lng
        self.date = date
        self.aqi = aqi


def load_db_from_csv(file_name: str):
    # Delete All Entries in Sites
    results = Site.query.all()
    for res in results:
        db.session.delete(res)
    db.session.commit()

    with open('daily_88101_2015.csv') as csvfile:
        reader = csv.DictReader(csvfile)

        counter = 0

        for row in reader:
            site_num = int(row['Site Num'])
            lat = float(row['Latitude'])
            lng = float(row['Longitude'])
            date = datetime.strptime(row['Date Local'], app.config['DATE_FORMAT'])
            aqi = int(row['AQI'] if row['AQI'] != '' else -1)

            obj = Site(site_num, lat, lng, date, aqi)
            db.session.add(obj)

            counter += 1
            if (counter > 10000):
                db.session.commit()
                counter = 0

        if counter > 0:
            db.session.commit()


@app.route('/', methods = ['POST', 'GET'])
def display2016():
    startdate = request.form['startdate']
    enddate = request.form['enddate']
    return render_template('map.html', startdate=startdate, enddate=enddate)


@app.route('/data', methods=['POST'])
def query_data():
    date = datetime.strptime(request.form['date'], app.config['DATE_FORMAT'])
    results = Site.query.filter(Site.date == date, Site.aqi != -1).all()

    def transform(element: Site):
        return {
            'lat': element.lat,
            'lng': element.lng,
            'aqi': element.aqi
        }

    return json.dumps(list(map(transform, results)))


@app.route('/form')
def selectDays():
    return render_template('form.html')

@app.route('/map')
def displaymap():
    return render_template('map2.html')

if __name__ == '__main__':
    db.create_all()
    if (app.config['LOAD_FROM_CSV']):
        load_db_from_csv('daily_88101_2015.csv')
    app.run(debug = True)