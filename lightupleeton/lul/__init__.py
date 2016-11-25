import os

IS_DEPLOYED = os.environ.get('SERVER_SOFTWARE', '').startswith('Google App Engine')