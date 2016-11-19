from google.appengine.ext import ndb

import lul.cron.handlers
import lul.models


class Migrate(lul.cron.handlers.Base):
        
    def get(self):
        
        to_save = []

        locations_to_migrate = lul.models.Location.all().filter(
            "migrated =", False
        ).fetch(limit=5)

        for location_to_migrate in locations_to_migrate:
            location_to_migrate.migrated = True
            to_save.append(location_to_migrate)

            new_poi = lul.models.PointOfInterest.create_from_location(location_to_migrate)
            to_save.append(new_poi)

        if to_save:
            ndb.put_multi(to_save)
