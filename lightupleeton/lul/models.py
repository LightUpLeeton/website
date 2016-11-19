from datetime import datetime

from google.appengine.ext import db
from google.appengine.ext import ndb
from google.appengine.api import users

from geo.geomodel import GeoModel

class Location(GeoModel):
    address = db.StringProperty(required=True)
    created_date = db.DateTimeProperty(auto_now_add=True)
    updated_date = db.DateTimeProperty(auto_now=True)
    added_by_committee = db.BooleanProperty(default=False)
    migrated = db.BooleanProperty(default=False)

class POILocation(ndb.Model):
    description = ndb.StringProperty(required=True)
    geo_point = ndb.GeoPtProperty(required=True)

    @property
    def address(self):
        return self.description

    @property
    def latitude(self):
        return self.geo_point.lat

    @property
    def longitude(self):
        return self.geo_point.lon

class PointOfInterest(ndb.Model):
    
    location = ndb.StructuredProperty(POILocation, required=True)
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    updated_date = ndb.DateTimeProperty(auto_now=True)
    added_by_committee = ndb.BooleanProperty(default=False)

    @property
    def current(self):
        now = datetime.now()
        return self.updated_date.year == now.year and not self.added_by_committee

    @classmethod
    def create_from_location(cls, location_to_migrate):
        
        poi_location = POILocation(
            description=location_to_migrate.address,
            geo_point=ndb.GeoPt(
                location_to_migrate.location.lat,
                location_to_migrate.location_to_migrate.lon
            )
        )

        poi = cls(
            location=poi_location,
            created_date=location_to_migrate.created_date,
            updated_date=location_to_migrate.updated_date,
            added_by_committee=location_to_migrate.added_by_committee
        )

        return poi

    @classmethod
    def create(cls, location_rest):
        
        poi_location = POILocation(
            description=location_rest.address,
            geo_point=ndb.GeoPt(
                location_rest.latitude,
                location_rest.longitude
            )
        )

        poi = cls(
            location=poi_location
        )

        return poi
