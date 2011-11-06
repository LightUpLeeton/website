import os

from prestans import *
from y2t.rest.handlers import *

from google.appengine.ext.webapp.util import run_wsgi_app

def main():

        rest_application = rest.JSONRESTApplication([
                (r'/api/listing/*([0-9]*|all)/*', ListingRESTHandler),
                (r'/api/listing/*([0-9]*)/*image/*([0-9]*|all)/*', ListingImageRESTHandler),
                (r'/api/category/*([0-9]*|all)/*', CategoryRESTHandler),
                (r'/api/message/*([0-9]*|all)/*', MessageRESTHandler),
        ])

        run_wsgi_app(rest_application)
        
if __name__ == "__main__":
        main()