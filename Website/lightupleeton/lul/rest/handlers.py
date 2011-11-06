from google.appengine.api import users
from google.appengine.ext import db
from prestans import handlers, rest
import lul.models
import lul.rest.models
import lul.rest.parsers

class LocationRESTRequestHandler(handlers.RESTRequestHandler):
    
    request_parser = lul.rest.parsers.LocationRequestParser()
    
    def create_or_fetch_location(self, address):
        
        model = lul.models.Location()
        
        return model
    
    def as_rest_model(self, persistent_model):
        
        rest_model = lul.rest.models.Location()
        
        rest_model.address = persistent_model.address
        
        return rest_model
        
    def as_rest_models(self, persistent_models):
        
        rest_models = list()
        for persistent_model in persistent_models:
            rest_models.append(self.as_rest_model(persistent_model))
        return rest_models

    def get(self, location_id):
        self.response.http_status = rest.STATUS.OK
        self.response.set_body_attribute('message', 'Location REST')
    def post(self, location_id):
        location_rest = self.request.parsed_body_model
    
        location_persistent = self.create_or_fetch_location(location_rest.address)
        location_persistent.address = location_rest.address
        location_persistent.location = db.GeoPt(location_rest.latitude, location_rest.longitude)
        
        #Check if user is logged in, then it must be submitted by committee
        if users.get_current_user():
            location_persistent.added_by_committee = True
    
    
        self.response.http_status = rest.STATUS.OK
        self.response.set_body_attribute('results', location_rest)
    def put(self, location_id):
        location_rest = self.request.parsed_body_model
    
        self.response.http_status = rest.STATUS.OK
        self.response.set_body_attribute('message', location_rest)
    def delete(self, location_id):
        self.response.http_status = rest.STATUS.OK
        self.response.set_body_attribute('message', 'Location REST')
