#Import dependencies

import numpy as np

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitations"""
    # Query all precipitations
    results = session.query(Measurement.date, Measurement.pcrp).all()

    session.close()

    # Convert list of tuples into normal list
    all_pcrp = list(np.ravel(results))

    return jsonify(all_pcrp)

 # Create a dictionary from the precipitation data using date as the key and prcp as the value
    #all_s = []
    #for name, age, sex in results:
       # passenger_dict = {}
        #passenger_dict["name"] = name
        #passenger_dict["age"] = age
        #passenger_dict["sex"] = sex
        #all_passengers.append(passenger_dict)

    #return jsonify(all_passengers)



@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query().all()

    session.close()

    # Convert list of tuples into normal list
    all_stationss = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def temperatures():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observations"""
    # Query dates and temp observations of the most active station for the last year of data

    results = session.query(Measurement.date, Measurement.tops).all()

    session.close()

    all_temps = list(np.ravel(results))

    return jsonify(all_temps)

   

if __name__ == '__main__':
    app.run(debug=True)