#Import dependencies

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end>"
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

    #temp_results = session.query(Measurement.date).all()
    year_ago = dt.datetime(2017,8,23) - dt.timedelta(days=365)
    one_year = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago).all()

    max_active=session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date>= year_ago).\
        filter(Measurement.station == 'USC00519281').all()

    session.close()

    all_temps = list(np.ravel(max_active))

    return jsonify(all_temps)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return min temp, max temp and avg temp for dates greater than a specific start date
    # Date is in the format Year-Month-Day

    st_date = dt.datetime.strptime(start, '%Y-%m-%d')
  
    date_results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date>= st_date).all()

    session.close()

    all_st_dates=list(np.ravel(date_results))
    
    return jsonify(date_results)    

   

def temp_start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return min temp, max temp and avg temp for dates greater than a specific start date
    # Date is in the format Year-Month-Day

    st_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
  
    end_date_results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date>= st_date).\
        filter(Measurement.date <=end_date).all()    

    return jsonify(end_date_results)    

    session.close()

   
   

if __name__ == '__main__':
    app.run(debug=True)