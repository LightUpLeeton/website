from google.appengine.ext import db

class Location(db.Model):
    address = db.StringProperty(required=True)