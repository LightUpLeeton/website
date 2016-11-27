from google.appengine.ext import ndb

import lul.cron.handlers
import lul.models


class Touch(lul.cron.handlers.Base):

    def get(self):

        pois = lul.models.PointOfInterest.query().fetch(limit=1000)
        ndb.put_multi(pois)