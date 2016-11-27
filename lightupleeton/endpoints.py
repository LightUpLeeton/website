import webapp2

import prestans.rest

import lul.page.handlers.html
import lul.page.handlers.pdf
import lul.rest.handlers.location

web = webapp2.WSGIApplication([
    ('/', lul.page.handlers.html.Main),
    ('/full', lul.page.handlers.html.Full),
    ('/locations', lul.page.handlers.html.Locations),

    ('/guide', lul.page.handlers.html.Guide)
])

api = prestans.rest.RequestRouter([
    (r'/api/location', lul.rest.handlers.location.Collection)
])