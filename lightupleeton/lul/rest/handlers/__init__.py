import prestans.rest


class Base(prestans.rest.RequestHandler):

    def handler_will_run(self):
        pass

    def handler_did_run(self):
        pass