from google.appengine.ext import db
from geo.geomodel import GeoModel

class Location(GeoModel):
    address = db.StringProperty(required=True)
    created_date = db.DateTimeProperty(auto_now_add=True)
    updated_date = db.DateTimeProperty(auto_now=True)
    added_by_committee = db.BooleanProperty(default=False)
