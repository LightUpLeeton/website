from prestans import parsers, types
from lul.rest import models


class LocationAllParameterSet(parsers.ParameterSet):
    offset = types.Integer(required=True, default=0)
    limit = types.Integer(required=True, default=10)

class LocationRequestParser(parsers.RequestParser):
    GET = parsers.ParserRuleSet(
        parameter_sets = [
            LocationAllParameterSet(),
        ]
    )
        
    POST = parsers.ParserRuleSet(
        body_template=models.Location()
    )

    PUT = parsers.ParserRuleSet(
        body_template=models.Location()
    )

    DELETE = parsers.ParserRuleSet(
        body_template=models.Location()
    )