import pandas as pd
from .database import SessionLocal, Base, engine
from .models import Sighting

# engine is result from create_engine method in database.py
# base is foundation for all db models
# (blueprint for tables)
# SessionLocal creates db sessions (live connection)

dataframe = pd.read_excel("data/sightings.xlsx")

print(dataframe.columns)
print(dataframe.head())

def clean_row(row):
    # takes single row from dataframe
    # return dictionary with clean python values
    # return None if row is invalid
    try:
        sighting_id = str(row["id"])
        date = pd.to_datetime(row["date"]).to_pydatetime()
        location = str(row["location"])
        species = str(row["species"])
        latinName = str(row["latinName"])
        return {
            "id" : sighting_id,
            "date" : date,
            "location" : location,
            "species" : species,
            "latinName" : latinName
        }

    
    except Exception as e:
        print("Exception caught")
        return None


Base.metadata.create_all(bind=engine)
db = SessionLocal()

for index, row in dataframe.iterrows():
    cleaned = clean_row(row)
    #if no rows at all
    if cleaned is None:
        continue

    #if current row already exists in db
    # first() (returns first match or nothing if nothing exists)
    existing = db.query(Sighting).filter(Sighting.id == cleaned["id"]).first()
    if existing:
        continue

    db.add(Sighting(**cleaned))

db.commit()
db.close()
print("Dataset loaded into database")