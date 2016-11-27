import lul.models
import lul.page.handlers


class Main(lul.page.handlers.Base):
    def get(self):

        template_values = {
            "GOOGLE_API_KEY": self.google_api_key
        }
        
        self.render_template("web", template_values)


class Full(lul.page.handlers.Base):
    def get(self):
        template_values = {
            "GOOGLE_API_KEY": self.google_api_key
        }
        
        self.render_template("web-full", template_values)


class Locations(lul.page.handlers.Base):
    def get(self):
        
        locations = lul.models.PointOfInterest.query().order(
            -lul.models.PointOfInterest.updated_date
        )

        template_values = {
            "locations_count": locations.count(),
            "locations": locations
        }

        self.render_template("web-locations", template_values)


LEETON_MIN_LAT = -34.57432351042673
LEETON_MAX_LAT = -34.53155583908121
LEETON_MIN_LNG = 146.38411045074463
LEETON_MAX_LNG = 146.42093181610107


class Guide(lul.page.handlers.Base):

    def generate_marker_string(self, pois, colour="red", precision=4):

        # fallback for no markers
        if pois.count() == 0:
            return ""

        marker_string = "&markers=color:%s" % colour
        for poi in pois:

            # exclude if outside acceptable ranges
            if poi.location.latitude < LEETON_MIN_LAT or \
               poi.location.latitude > LEETON_MAX_LAT or \
               poi.location.longitude < LEETON_MIN_LNG or \
               poi.location.longitude > LEETON_MAX_LNG:
                continue

            marker_string += "%%7C%f,%f" % (poi.location.latitude, poi.location.longitude)

        return marker_string

    def get(self):

        leeton_pois = lul.models.PointOfInterest.query()

        template_values = {
            "GOOGLE_API_KEY": self.google_api_key,
            "CENTRE": "-34.553,146.400",
            "LEETON_MARKERS": self.generate_marker_string(leeton_pois),
            "ZOOM": 14
        }

        self.render_template("guide", template_values)


class LetsEncryptHandler(lul.page.handlers.Base):

    def get(self, challenge):
        self.response.headers['Content-Type'] = 'text/plain'
        responses = {
                    'p3w4zOwxmf2SherSZ7tOtTkrvYL45y156essjJFMW5o': 'p3w4zOwxmf2SherSZ7tOtTkrvYL45y156essjJFMW5o.HNbU1uUcwn5AWt_OMA6FoJBkcibXcKeRi_W6eT3LRq8'
                }
        self.response.write(responses.get(challenge, ''))

