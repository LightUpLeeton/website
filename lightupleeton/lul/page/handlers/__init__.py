# -*- coding: utf-8 -*-
import jinja2
import webapp2


class Base(webapp2.RequestHandler):

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