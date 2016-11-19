from prestans import types

class Base(types.Model):
    pass 

class Location(types.Model):
    address = types.String(required=True)
    latitude = types.Float(required=True)
    longitude = types.Float(required=True)

class PointOfInterest(Base):
    location = Location(required=True)
    current = types.Boolean(required=True, default=False)
    