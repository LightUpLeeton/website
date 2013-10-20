__all__ = ["handlers", "parsers", "models", "api"]

import prestans.rest
import handlers.location
#import logging

#logging.getLogger().setLevel(logging.DEBUG)

api = prestans.rest.JSONRESTApplication([
	(r'/api/location', handlers.location.Collection)
])