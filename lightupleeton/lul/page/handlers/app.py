import lul.page.handlers

from google.appengine.ext.webapp import template
import os

import lul.models

class Main(lul.page.handlers.Base):
    def get(self):        
        template_values = {}
        
        path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'static', 'html', 'web.html')
        self.response.out.write(template.render(path, template_values))


class Full(lul.page.handlers.Base):
    def get(self):
        template_values = {}
        
        path = os.path.join(os.path.dirname(__file__),'..', '..', '..', 'static', 'html', 'web-full.html')
        self.response.out.write(template.render(path, template_values))


class Locations(lul.page.handlers.Base):
    def get(self):
        
        template_values = {
            "locations": lul.models.Location.all().order("-updated_date")
        }
        
        path = os.path.join(os.path.dirname(__file__),'..', '..', '..', 'static', 'html', 'locations-web.html')
        self.response.out.write(template.render(path, template_values))
        
class Manage(lul.page.handlers.Base):
    def get(self):
        
        template_values = {}
        
        path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'static', 'html', 'manage-web.html')
        self.response.out.write(template.render(path, template_values))
