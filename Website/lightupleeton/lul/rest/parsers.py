from prestans import parsers, types
from lul.rest import models


class LocationSearchParameterSet(parsers.ParameterSet):
    latitude = types.Float(required=True)
    longitude = types.Float(required=True)
    radius = types.Float(required=True, default=5.0)

class LocationRequestParser(parsers.RequestParser):        
    POST = parsers.ParserRuleSet(
        body_template=models.Location()
    )

    PUT = parsers.ParserRuleSet(
        body_template=models.Location()
    )

    DELETE = parsers.ParserRuleSet(
        body_template=models.Location()
    )