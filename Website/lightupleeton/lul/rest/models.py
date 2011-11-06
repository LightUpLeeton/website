from prestans import types

class Location(types.Model):
    id = types.Integer(required=False, identifier=True)
    address = types.String(required=True)
    latitude = types.Float(required=True)
    longitude = types.Float(required=True)
    current = types.Boolean(required=True, default=False)
    
class Test(types.Model):
    id = types.Integer(required=True, default=1)
    