from webapp2 import Route

routes = [    
    # OpenID login
    Route('/_ah/login_required','openid.views.openid_handler.OpenIDHandler', name='openid-login'),

]