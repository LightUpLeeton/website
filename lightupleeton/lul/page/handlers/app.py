import lul.page.handlers

from google.appengine.ext.webapp import template
import os

import lul.models


class Main(lul.page.handlers.Base):
    def get(self):      
        template_values = {}
        
        self.render_template("web", template_values)


class Full(lul.page.handlers.Base):
    def get(self):
        template_values = {}
        
        self.render_template("web-full", template_values)


class Locations(lul.page.handlers.Base):
    def get(self):
        
        locations = lul.models.PointOfInterest.query().order(
            -lul.models.PointOfInterest.updated_date
        )

        template_values = {
            "locations": locations
        }

        self.render_template("web-locations", template_values)
