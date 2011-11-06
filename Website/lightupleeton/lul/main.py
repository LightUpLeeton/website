#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

import os, re

class MainHandler(webapp.RequestHandler):
    def get(self):        
        template_values = {}
        
        #Check for mobile or web version by domain name
        
        path = os.path.join(os.path.dirname(__file__), '..', 'static', 'html', 'web.html')
        self.response.out.write(template.render(path, template_values))
class ManageHandler(webapp.RequestHandler):
    def get(self):
        
        template_values = {}
        
        #Check for mobile or web version by domain name
        
        path = os.path.join(os.path.dirname(__file__), '..', 'static', 'html', 'manage-web.html')
        self.response.out.write(template.render(path, template_values))


def main():
    application = webapp.WSGIApplication([('/', MainHandler), ('/manage', ManageHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
