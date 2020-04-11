from flask import Flask, jsonify
import datetime
from datetime import timedelta
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

Base = automap_base()

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base.prepare(engine, reflect=True)

# Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and prcp measurements"""
    # Query all dates and prcp measurements
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    date_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        date_prcp.append(prcp_dict)

    return jsonify(date_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # Query the dates and temperature observations of the most active station for the last year of data.

    last_date_query = session.query(Measurement).order_by(Measurement.date.desc()).first()
    last_date = last_date_query.date

    one_year_ago = (datetime.datetime.strptime(last_date, '%Y-%m-%d') - timedelta(days=365)).strftime('%Y-%m-%d')

    USC00519281_temps = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
                    order_by(Measurement.date.desc()).\
                    filter(Measurement.date<=last_date).\
                    filter(Measurement.date>=one_year_ago).\
                    filter(Measurement.station=='USC00519281').all()

    session.close()

    return jsonify(USC00519281_temps)

@app.route("/api/v1.0/<start>")
def temp_info_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    lowest_temp = session.query(Measurement.date, func.min(Measurement.tobs).label('Lowest Temp')).\
                filter(Measurement.date >= start)

    # for row in lowest_temp:
    #     print(f'The lowest temperature recorded by USC00519281 was {row[1]}.')

    highest_temp = session.query(Measurement.date, func.max(Measurement.tobs).label('Highest Temp')).\
                filter(Measurement.date >= start)

    # for row in highest_temp:
    #     print(f'The highest temperature recorded by USC00519281 was {row[1]}.')

    avg_temp = session.query(Measurement.date, func.avg(Measurement.tobs).label('Avgerage Temp')).\
                filter(Measurement.date >= start)

    # for row in avg_temp:
    #     print(f'The average temperature recorded by USC00519281 was {round(row[1], 2)}.')
    
    session.close()

    low = ""
    low_date = ""
    high = ""
    high_date = ""
    avg = ""

    for date_low in lowest_temp:
        
        low = date_low[1]
        low_date = date_low[0]

    for date_high in highest_temp:

        high = date_high[1]
        high_date = date_high[0]
        
    for date_avg in avg_temp:

        avg = (round(date_avg[1], 2))

    return jsonify(f'For all dates after {start}, the low temperature was {low}, on {low_date}, the high temperature was {high}, on {high_date}, the average temperature was {avg}')

@app.route("/api/v1.0/<start>/<end>")
def temp_info_startend(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    lowest_temp = session.query(Measurement.date, func.min(Measurement.tobs).label('Lowest Temp')).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end)

    # for row in lowest_temp:
    #     print(f'The lowest temperature recorded by USC00519281 was {row[1]}.')

    highest_temp = session.query(Measurement.date, func.max(Measurement.tobs).label('Highest Temp')).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end)

    # for row in highest_temp:
    #     print(f'The highest temperature recorded by USC00519281 was {row[1]}.')

    avg_temp = session.query(Measurement.date, func.avg(Measurement.tobs).label('Avgerage Temp')).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end)

    # for row in avg_temp:
    #     print(f'The average temperature recorded by USC00519281 was {round(row[1], 2)}.')
    
    session.close()

    low = ""
    low_date = ""
    high = ""
    high_date = ""
    avg = ""

    for date_low in lowest_temp:
        
        low = date_low[1]
        low_date = date_low[0]

    for date_high in highest_temp:

        high = date_high[1]
        high_date = date_high[0]
        
    for date_avg in avg_temp:

        avg = (round(date_avg[1], 2))

    return jsonify(f'For all dates between {start} and {end}, the low temperature was {low}, on {low_date}, the high temperature was {high}, on {high_date}, the average temperature was {avg}')

if __name__ == '__main__':
    app.run(debug=True)