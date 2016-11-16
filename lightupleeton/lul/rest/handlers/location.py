from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import db

import prestans.parser
import prestans.types

import lul.models
import lul.rest.models
import lul.rest.handlers

from geo import *
from datetime import datetime
import re

ALL_LOCATIONS_CACHE_KEY = "all_locations_cache_key"

class SearchParameterSet(prestans.parser.ParameterSet):
    latitude = prestans.types.Float(required=True)
    longitude = prestans.types.Float(required=True)
    radius = prestans.types.Float(required=True, default=5.0)

create_filter = prestans.parser.AttributeFilter.from_model(lul.rest.models.Location())
create_filter.address = True

class Collection(lul.rest.handlers.Base):
    
    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            parameter_sets=[SearchParameterSet()],
            response_template=prestans.types.Array(
                element_template=lul.rest.models.Location()
            )
        ),
        POST=prestans.parser.VerbConfig(
            request_attribute_filter=create_filter,
            body_template=lul.rest.models.Location(),
            response_template=lul.rest.models.Location()
        )
    )
    
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
        
    def get(self):
    
        locations_rest = memcache.get(ALL_LOCATIONS_CACHE_KEY)
        if locations_rest is None:
            locations = lul.models.Location.all()
            locations_rest = self.as_rest_models(locations)
            memcache.set(ALL_LOCATIONS_CACHE_KEY, locations_rest)
        
        self.response.http_status = rest.STATUS.OK
        self.response.set_body_attribute('results', locations_rest)
    
    def post(self):
        location_rest = self.request.parsed_body_model
        
        if re.match("^.*(Leeton NSW 2705, Australia|Yanco NSW 2703, Australia|Whitton NSW 2705, Australia)$", location_rest.address) is None:
            self.response.http_status = rest.STATUS.BAD_REQUEST
            self.response.set_body_attribute('message', 'Light Up Leeton only accepts addresses from Leeton, Whitton and Yanco')
            return
        
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
        memcache.delete(ALL_LOCATIONS_CACHE_KEY)
        locations = lul.models.Location.all()
        locations_rest = self.as_rest_models(locations)
        memcache.set(ALL_LOCATIONS_CACHE_KEY, locations_rest)
    
        self.response.http_status = rest.STATUS.OK
        self.response.set_body_attribute('results', self.as_rest_models([location_persistent]))