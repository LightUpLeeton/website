__all__ = ["rest", "models", "app"]

from google.appengine.ext.webapp import template

import os, re, urlparse, webapp2

import lul.models

class MainHandler(webapp2.RequestHandler):
    def get(self):        
        template_values = {}
        
        #Check for mobile or web version by domain name
        #url = urlparse.urlparse(self.request.url)
        #import logging
        #logging.warn(url.netloc)
        
        path = os.path.join(os.path.dirname(__file__), '..', 'static', 'html', 'web.html')
        self.response.out.write(template.render(path, template_values))

class LocationsHandler(webapp2.RequestHandler):
    def get(self):
        
        template_values = {
            "locations": lul.models.Location.all().order("-updated_date")
        }
        
        path = os.path.join(os.path.dirname(__file__), '..', 'static', 'html', 'locations-web.html')
        self.response.out.write(template.render(path, template_values))
        
class ManageHandler(webapp2.RequestHandler):
    def get(self):
        
        template_values = {}
        
        #Check for mobile or web version by domain name
        #import urlparse
        
        path = os.path.join(os.path.dirname(__file__), '..', 'static', 'html', 'manage-web.html')
        self.response.out.write(template.render(path, template_values))



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/locations', LocationsHandler),
    ('/manage', ManageHandler)
])