import webapp2

import prestans.rest

import lul.cron.handlers.point_of_interest
import lul.page.handlers.html
import lul.rest.handlers.location

web = webapp2.WSGIApplication([
    ('/', lul.page.handlers.html.Main),
    ('/full', lul.page.handlers.html.Full),
    ('/locations', lul.page.handlers.html.Locations),

    ('/guide', lul.page.handlers.html.Guide)
])

cron = prestans.rest.RequestRouter([
    (r'/cron/point-of-interest/touch', lul.cron.handlers.point_of_interest.Touch)
])

api = prestans.rest.RequestRouter([
    (r'/api/location', lul.rest.handlers.location.Collection)
])