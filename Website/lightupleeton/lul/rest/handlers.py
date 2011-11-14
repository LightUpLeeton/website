from google.appengine.api import users
from google.appengine.ext import db
from prestans import handlers, rest, types
import lul.models
from lul.rest import parsers
import lul.rest.models
#import lul.rest.parsers
from geo import *
from datetime import datetime



class LocationRESTRequestHandler(handlers.RESTRequestHandler):
    
    request_parser = parsers.LocationRequestParser()
    
    def as_rest_model(self, persistent_model):
        
        rest_model = lul.rest.models.Location()
        
        rest_model.id = persistent_model.key().id()
        rest_model.address = persistent_model.address
        rest_model.latitude = persistent_model.location.lat
        rest_model.longitude = persistent_model.location.lon
        rest_model.current = persistent_model.updated_date.year == datetime.now().year and not persistent_model.added_by_committee
        
        return rest_model
        
    def as_rest_models(self, persistent_models):
        
        rest_models = types.Array(element_template=lul.rest.models.Location())
        for persistent_model in persistent_models:
            rest_models.append(self.as_rest_model(persistent_model))
        return rest_models

    def locations_around_point(self, latitude, longitude, radius = 10.0):
                results = lul.models.Location.proximity_fetch(
                        lul.models.Location.all(),
                        geotypes.Point(latitude, longitude),
                        max_results = 200,
                        max_distance = radius * 1000
                )
                return results;
        
    def get(self, location_id):
    
        if isinstance(self.request.parameter_set, lul.rest.parsers.LocationSearchParameterSet):
            locations = self.locations_around_point(self.request.parameter_set.latitude, self.request.parameter_set.longitude, self.request.parameter_set.radius)
        
            self.response.http_status = rest.STATUS.OK
            self.response.set_body_attribute('results', self.as_rest_models(locations))
        else:
            self.response.http_status = rest.STATUS.NOT_FOUND
            self.response.set_body_attribute('message', 'Unsupported Request')
    
    def post(self, location_id):
        location_rest = self.request.parsed_body_model
        
        location_query = lul.models.Location.all().filter("address =", location_rest.address)
        locations = location_query.fetch(location_query.count())
        
        if len(locations) > 0:
            location_persistent = locations[0]
        else:
            location_persistent = lul.models.Location(
                address=location_rest.address
            )
        
        location_persistent.location = db.GeoPt(location_rest.latitude, location_rest.longitude)
        
        #Check if user is logged in, then it must be submitted by committee
        if users.get_current_user():
            location_persistent.added_by_committee = True
        
        location_persistent.update_location()
        location_persistent.put()
    
        self.response.http_status = rest.STATUS.OK
        self.response.set_body_attribute('results', self.as_rest_models([location_persistent]))
    def put(self, location_id):
        location_rest = self.request.parsed_body_model
    
        self.response.http_status = rest.STATUS.OK
        self.response.set_body_attribute('message', location_rest)
    def delete(self, location_id):
        self.response.http_status = rest.STATUS.OK
        self.response.set_body_attribute('message', 'Location REST')
