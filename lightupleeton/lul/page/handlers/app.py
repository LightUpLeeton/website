from google.appengine.ext.webapp import template
import os

import lul.models
import lul.page.handlers


class Main(lul.page.handlers.Base):
    def get(self):

        template_values = {
            "GOOGLE_API_KEY": self.google_api_key
        }
        
        self.render_template("web", template_values)


class Full(lul.page.handlers.Base):
    def get(self):
        template_values = {
            "GOOGLE_API_KEY": self.google_api_key
        }
        
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

class LetsEncryptHandler(lul.page.handlers.Base):

    def get(self, challenge):
        self.response.headers['Content-Type'] = 'text/plain'
        responses = {
                    'p3w4zOwxmf2SherSZ7tOtTkrvYL45y156essjJFMW5o': 'p3w4zOwxmf2SherSZ7tOtTkrvYL45y156essjJFMW5o.HNbU1uUcwn5AWt_OMA6FoJBkcibXcKeRi_W6eT3LRq8'
                }
        self.response.write(responses.get(challenge, ''))
