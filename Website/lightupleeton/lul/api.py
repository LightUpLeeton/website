from prestans import rest
from lul.rest import handlers

from google.appengine.ext.webapp.util import run_wsgi_app

def main():

        rest_application = rest.JSONRESTApplication([
                (r'/api/location/*([0-9]*|all)/*', handlers.LocationRESTRequestHandler)
        ])

        run_wsgi_app(rest_application)
        
if __name__ == "__main__":
        main()