import logging
import os
#from google.appengine.ext.webapp import template
from google.appengine.api import users
import webapp2
from webapp2_extras import jinja2, sessions 
from openid.openid import *



class OpenIDHandler(webapp2.RequestHandler):
    """
    Login and redirect back.
    
    """
    def get(self):
        """ login prompt
        
        """
        redirect_uri = self.request.get('continue') 
        user = users.get_current_user()
        
        if not user:
            
            openid_logins = generate_login_urls(dest_url=redirect_uri)
            
            return self.render_html_response(
                'openid_login.html',
                openid_providers = openid_logins,
                redirect_uri = redirect_uri
            )
            
            
        if redirect_uri:
            self.redirect(str(redirect_uri))
            
    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        jinja2_obj = jinja2.get_jinja2(app=self.app)
        
        return jinja2_obj


    def render_html_response(self, template, http_code=200, **context):
        """Renders a Jinja2 template with the given context"""
        
        rv = self.jinja2.render_template(template, **context)
        self.response.write(rv)
        self.response.status = http_code

routes = [
]

# openid URLS
from openid.urls import routes as openid_routes
routes.extend(openid_routes)

app = webapp2.WSGIApplication(
    routes,
    debug=False
)

def main():
    app.run()
    
if __name__ == '__main__':
    main()