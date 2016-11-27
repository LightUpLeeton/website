from google.appengine.ext import db
from google.appengine.ext import ndb

import lul.cron.handlers
import lul.models


class MigrateReset(lul.cron.handlers.Base):

    def get(self):

        to_save = []
        locations_to_migrate = lul.models.Location.all().fetch(limit=1000)

        for location in locations_to_migrate:
            location.migrated = False
            to_save.append(location)

        if to_save:
            db.put(to_save)


class Migrate(lul.cron.handlers.Base):
        
    def get(self):
        
        db_to_save = []
        ndb_to_save = []

        locations_to_migrate = lul.models.Location.all().filter(
            "migrated =", False
        ).fetch(limit=1000)

        import logging
        logging.error("found %i locations to migrate" % len(locations_to_migrate))

        for location_to_migrate in locations_to_migrate:

            # skip if already migrated
            if location_to_migrate.migrated:
                break

            location_to_migrate.migrated = True
            db_to_save.append(location_to_migrate)

            new_poi = lul.models.PointOfInterest.create_from_location(location_to_migrate)
            ndb_to_save.append(new_poi)

        if ndb_to_save:
            ndb.put_multi(ndb_to_save)

        if db_to_save:
            db.put(db_to_save)
