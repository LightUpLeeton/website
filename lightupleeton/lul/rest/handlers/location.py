from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import db

import prestans.ext.data.adapters.ndb
import prestans.parser
import prestans.rest
import prestans.types

import lul.models
import lul.rest.adapters
import lul.rest.models
import lul.rest.handlers

from geo import *
from datetime import datetime
import re

ALL_POI_CACHE_KEY = "all_poi_cache_key"

class SearchParameterSet(prestans.parser.ParameterSet):
    latitude = prestans.types.Float(required=False)
    longitude = prestans.types.Float(required=False)
    radius = prestans.types.Float(required=True, default=5.0)

create_filter = prestans.parser.AttributeFilter.from_model(lul.rest.models.Location())
create_filter.address = True
create_filter.latitude = True
create_filter.longitude = True

class Collection(lul.rest.handlers.Base):
    
    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            parameter_sets=[SearchParameterSet()],
            response_template=prestans.types.Array(
                element_template=lul.rest.models.PointOfInterest()
            ),
            response_attribute_filter_default_value=True
        ),
        POST=prestans.parser.VerbConfig(
            request_attribute_filter=create_filter,
            body_template=lul.rest.models.Location(),
            response_template=lul.rest.models.PointOfInterest()
        )
    )
        
    def get(self):

        pois_rest = memcache.get(ALL_POI_CACHE_KEY)
        if pois_rest is None:
            pois = lul.models.PointOfInterest.query()

            pois_rest = prestans.ext.data.adapters.ndb.adapt_persistent_collection(
                pois,
                lul.rest.models.PointOfInterest,
                self.response.attribute_filter
            )
            memcache.set(ALL_POI_CACHE_KEY, pois_rest)

        self.response.status = prestans.http.STATUS.OK
        self.response.body = pois_rest
    
    def post(self):
        location_rest = self.request.parsed_body
        
        # ensure address is located in valid towns
        if re.match("^.*(Leeton NSW 2705, Australia|Yanco NSW 2703, Australia|Whitton NSW 2705, Australia)$", location_rest.address) is None:
            raise prestans.exception.BadRequest("Light Up Leeton only accepts addresses from Leeton, Whitton and Yanco")
        
        # check for an existing location with same address
        poi = lul.models.PointOfInterest.query().filter(
            lul.models.PointOfInterest.location.description==location_rest.address
        ).get()
        
        if poi:
            poi.last_submitted_date = datetime.now()
            poi.put()
        else:
            poi = lul.models.PointOfInterest.create(location_rest)
            poi.put()
        
        memcache.delete(ALL_POI_CACHE_KEY)
    
        self.response.status = prestans.http.STATUS.CREATED
        self.response.body = prestans.ext.data.adapters.ndb.adapt_persistent_instance(
            poi,
            lul.rest.models.PointOfInterest,
            self.response.attribute_filter
        )
        
