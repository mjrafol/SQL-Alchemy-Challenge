# Set-up dependencies
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database set-up

# Set-up the connection
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask set-up

# Create the app
app = Flask(__name__)

# Create the home route
@app.route("/")
def homepage():

    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Search by Start Date Route (Format: /api/v1.0/YYYY-MM-DD):<br/>"
        f"/api/v1.0/<start><br/>"
        f"<br/>"
        f"Search by Start Date / End Date Route (Format: /api/v1.0/YYYY-MM-DD/YYYY-MM-DD):<br/>"
        f"/api/v1.0/<start>/<end>"
    )


# Create the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create variable for last year (per Rubric)
    last_yr_start = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Create the session 
    session = Session(engine)

    # Query results to a dictionary using `date` as the key and `prcp` as the value
    results =  session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_yr_start).all()

    # Create an empty list
    all_prcp = []

    # Loop through the results
    for date, prcp in results:

        # Each row is an object in dictionary
        prcp_dict = {}

        # Assigning the values for each column
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp

        # Add to list
        all_prcp.append(prcp_dict)
    
    return jsonify(all_prcp)


# Create the stations route
@app.route("/api/v1.0/stations")
def stations():

    # Create the session
    session = Session(engine)

    # Query all passengers (saves in a tuple)
    results = session.query(Station.station).all()

    # Close our session
    session.close()

    # Convert list of tuples into a normal list
    all_stations = list(np.ravel(results))

    # Return all names
    return jsonify(all_stations)


# Create the tobs route
@app.route("/api/v1.0/tobs")
def tobs():

    # Create the session 
    session = Session(engine)

    # Create variable for last year (per Rubric)
    last_yr_start = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query the dates and temperature observations of the most active station for the previous year of data
    results =  session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter((Measurement.date >= last_yr_start)).all()

    # Create an empty list
    active_station = []

    # Loop through the results
    for date, tobs in results:

        # Each row is an object in dictionary
        active_station_dict = {}

        # Assigning the values for each column
        active_station_dict["date"] = date
        active_station_dict["tobs"] = tobs

        # Add to list
        active_station.append(active_station_dict)
    
    return jsonify(active_station)


# Create the variable route based on start date
@app.route("/api/v1.0/<start>")
def start_date(start):

    # Create the session 
    session = Session(engine)

    # Query the temperature observations statistics based on start date
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    # Create an empty list
    tobs_stats = []

    # Loop through the results
    for TMIN, TMAX, TAVG in results:

        # Create an empty dictionary
        tobs_dict = {}

        # Assigning the dictionary key and values for each column
        tobs_dict["Minimum Temperature"] = TMIN
        tobs_dict["Maximum Temperature"] = TMAX
        tobs_dict["Average Temperature"] = TAVG

        # Add to tobs_stats list
        tobs_stats.append(tobs_dict)
    
    return jsonify(tobs_stats)


# Create the variable route based on start date
@app.route("/api/v1.0/<start>/<end>")
def filter_date(start, end):

    # Create the session 
    session = Session(engine)

    # Query the temperature observations statistics based on start and end date
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Create an empty list
    tobs_filter_stats = []

    # Loop through the results
    for TMIN, TMAX, TAVG in results:

        # Create an empty dictionary
        tobs_filter_dict = {}

        # Assigning the dictionary key and values for each column
        tobs_filter_dict["Minimum Temperature"] = TMIN
        tobs_filter_dict["Maximum Temperature"] = TMAX
        tobs_filter_dict["Average Temperature"] = TAVG

        # Add to tobs_stats list
        tobs_filter_stats.append(tobs_filter_dict)
    
    return jsonify(tobs_filter_stats)


#BOILERPLATE
if __name__ == "__main__":
    app.run(debug=True)