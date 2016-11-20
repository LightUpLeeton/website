import webapp2

import prestans.rest

import lul.page.handlers.app
import lul.cron.handlers.location
import lul.rest.handlers.location

app = webapp2.WSGIApplication([
    ('/', lul.page.handlers.app.Main),
    ('/full', lul.page.handlers.app.Full),
    ('/locations', lul.page.handlers.app.Locations)
])

cron = prestans.rest.RequestRouter([
    (r'/cron/location/migrate', lul.cron.handlers.location.Migrate),
    (r'/cron/location/migrate/reset', lul.cron.handlers.location.MigrateReset)
])

api = prestans.rest.RequestRouter([
    (r'/api/location', lul.rest.handlers.location.Collection)
])