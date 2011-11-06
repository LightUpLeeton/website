from prestans import types

class Location(types.Model):
    address = types.String(required=True)
    latitude = types.Float(required=False)
    longitude = types.Float(required=False)
    current = types.Boolean(required=True, default=False)