from prestans import handlers, rest

class LocationRESTRequestHandler(handlers.RESTRequestHandler):
    def get(self, location_id):
        self.response.http_status = rest.STATUS.OK
        self.response.set_body_attribute('message', 'Location REST')