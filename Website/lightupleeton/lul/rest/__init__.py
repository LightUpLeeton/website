__all__ = ["handlers", "parsers", "models", "api"]

from prestans import rest
from . import handlers

api = rest.JSONRESTApplication([(r'/api/location/*([0-9]*|all)/*', handlers.LocationRESTRequestHandler)])