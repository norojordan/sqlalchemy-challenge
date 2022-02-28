#Import dependencies

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to Hawaii's Weather Page<br>"
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Temperatures for one year: /api/v1.0/tobs<br>"
        f"Min, max and average temps for start date (yyyy-mm-dd): /api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a dictionary of dates and precipitations"""
    # Query all precipitations using date as the key and prcp as the value
    prcp_results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert results to a dictionary
    all_prcp = []
    for date, prcp in prcp_results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    st_results = session.query(Station.station, Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(st_results))

    return jsonify(all_stations)
    


@app.route("/api/v1.0/tobs")
def temperatures():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observations"""
    # Query dates and temp observations of the most active station for the last year of data

    year_ago = dt.datetime(2017,8,23) - dt.timedelta(days=365)
    one_year = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago).all()

    max_active=session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date>= year_ago).\
        filter(Measurement.station == 'USC00519281').all()

    session.close()

    all_temps = list(np.ravel(max_active))

    return jsonify(all_temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def temp_start(start=None, end='2017-08-23'):
    # If no end date is provided, default to last date in the database
    session = Session(engine)

    # Return min temp, max temp and avg temp for dates greater than a specific start date
    # Date is in the format Year-Month-Day

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    date_start = dt.datetime.strptime(start,"%Y-%m-%d")
    date_end = dt.datetime.strptime(end, "%Y-%m-%d")
    date_results=session.query(*sel).\
        filter(Measurement.date >= date_start).\
        filter(Measurement.date<=date_end).all()

    session.close()   

    sdateall = []
    for min, avg, max in date_results:
        sdate_dict = {}
        sdate_dict["Minimum Temperature"]=min
        sdate_dict["Average"]= avg
        sdate_dict["Maximum Temperature"] = max
        sdate_dict["Start Date"]=date_start
        sdate_dict["End Date"]=date_end
        sdateall.append(sdate_dict)


    
    return jsonify(sdateall)   
      
   
   

if __name__ == '__main__':
    app.run(debug=True)