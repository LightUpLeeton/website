import webapp2

import prestans.rest

import lul.page.handlers.app
import lul.rest.handlers.location

app = webapp2.WSGIApplication([
    ('/', lul.page.handlers.app.Main),
    ('/full', lul.page.handlers.app.Full),
    ('/locations', lul.page.handlers.app.Locations)
])

api = prestans.rest.RequestRouter([
	(r'/api/location', lul.rest.handlers.location.Collection)
])