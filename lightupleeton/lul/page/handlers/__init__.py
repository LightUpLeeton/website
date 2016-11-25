# -*- coding: utf-8 -*-
import jinja2
import os
import webapp2

import lul


class Base(webapp2.RequestHandler):

    @property
    def google_api_key(self):

        api_key = os.environ.get("GOOGLE_MAPS_DEVEL")
        if lul.IS_DEPLOYED:
            api_key = os.environ.get("GOOGLE_MAPS_PROD")

        return api_key

    @webapp2.cached_property
    def jinja2_env(self):
        return jinja2.Environment(
            loader=jinja2.PackageLoader("lul", "templates"),
            extensions=['jinja2.ext.autoescape'], 
            autoescape=False
        )

    def render_template(self, template_name, template_values=None, extension="html"):
        """Wrapper to render jinja2 template"""

        if template_values is None:
            template_values = {}

        template = self.jinja2_env.get_template("%s.%s" % (template_name, extension))
        self.response.out.write(template.render(**template_values))