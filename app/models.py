from sqlalchemy import Column, String, DateTime
from .database import Base

class Sighting(Base):
    __tablename__ = "sightings"

    id = Column(String, primary_key = True)
    date = Column(DateTime)
    location = Column(String)
    species = Column(String)
    latinName = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "location": self.location,
            "species": self.species,
            "latinName": self.latinName
        }



