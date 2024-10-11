
import sqlalchemy
from flask import Flask, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from datetime import datetime, timedelta

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine)

M = Base.classes.measurement
S = Base.classes.station

app = Flask(__name__)

@app.route('/')
def homepage():
    return '''
    <h1>Hawaii's Weather API</h1>
    <h4>Available routes:</h4>
    <ul>
        <li>/api/v1.0/precipitation</li>
        <li>/api/v1.0/stations</li>
        <li>/api/v1.0/tobs</li>
        <li>/api/v1.0/[start_date]</li>
        <li>/api/v1.0/[start_date]/[end_date]</li>
    </ul>  
    '''


@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    
    # Perform the query
    results = session.query(M.date, M.prcp).filter(M.date >= "2016-08-23").all()

    # Convert to a dictionary with date as the key
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
     # Perform the query
    results = session.query(S.station, S.name).all()

    # Convert to a dictionary with date as the key
    stations_data = {id: loc for id, loc in results}
    return jsonify(stations_data)


@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
   
    results = session.query(M.date, M.tobs).filter(M.date >= "2016-08-23").all()
    session.close()

    tobs_data = {date: tobs for date, tobs in results}
    return jsonify(tobs_data)

@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def stats(start, end=None):
    session = Session(engine)

    if not end:
        results = session.query(func.min(M.tobs), func.avg(M.tobs), func.max(M.tobs)).filter(M.date >= start).all()
    else:
        results = session.query(func.min(M.tobs), func.avg(M.tobs), func.max(M.tobs)).filter(M.date >= start).filter(M.date <= end).all()

    session.close()

    stats_data = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }
    return jsonify(stats_data)

if __name__ == '__main__':
    app.run(debug=True)


