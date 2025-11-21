from flask import Flask
from app.database import SessionLocal
from app.models import Sighting
from flask import request, jsonify
from datetime import datetime
from sqlalchemy import func



app = Flask(__name__)

@app.get("/")
def home():
    return "This is the home page. Please use /sightings, /stats/locations, /stats/monthlys, /stats/weekly or /stats/species"
@app.get("/sightings")
def get_sightings():
    db = SessionLocal()

    query = db.query(Sighting)

    location = request.args.get("location")
    if location:
        query = query.filter(Sighting.location == location)

    species = request.args.get("species")
    if species:
        query = query.filter(Sighting.species == species)

    start_date = request.args.get("start_date")
    if start_date:
        try:
            start = datetime.fromisoformat(start_date)
            query = query.filter(Sighting.date >= start)
        except ValueError:
            db.close()
            return jsonify({"error": "Invalid start_date format"}), 400

    end_date = request.args.get("end_date")
    if end_date:
        try:
            end = datetime.fromisoformat(end_date)
            query = query.filter(Sighting.date <= end)
        except ValueError:
            db.close()
            return jsonify({"error": "Invalid end_date format"}), 400

    #limit and offset
    limit = request.args.get("limit", type=int)
    offset = request.args.get("offset", type=int)

    if limit:
        query = query.limit(limit)

    if offset:
        query = query.offset(offset)


    rows = query.all() # gets rows from built queries above
    
    db.close()

    return jsonify([row.to_dict() for row in rows])

    

@app.get("/stats/locations")
def get_stats_locations():
    db = SessionLocal()

    query = db.query( 
        Sighting.location,
        func.count(Sighting.id)
        ).group_by(Sighting.location).all()
    
    db.close()

    return jsonify([{
        "location" : location,
        "count" : count}
        for location, count in query])

@app.get("/stats/monthly")
def get_stats_monthly():
    db = SessionLocal()

    month = func.strftime("%Y-%m", Sighting.date)
    query = db.query(month, func.count()).group_by(month).all()

    db.close()

    return jsonify([{
        "month" : month_value,
        "count" : count
    } for month_value, count in query])

@app.get("/stats/weekly")
def get_stats_weekly():
    db = SessionLocal()

    week = func.strftime("%Y-%W", Sighting.date)
    query = db.query(week, func.count()).group_by(week).all()

    db.close()

    return jsonify([{
        "week" : week_value,
        "count" : count
    } for week_value, count in query])    

    
@app.get("/stats/species")
def get_stats_species():
    db = SessionLocal()

    query = db.query(
        Sighting.species,
        func.count(Sighting.id)
        ).group_by(Sighting.species).order_by(func.count().desc()).all()

    db.close()

    return jsonify([{
        "species" : species,
        "count" : count
    } for species, count in query])

if __name__ == "__main__":
    app.run(debug=True)

