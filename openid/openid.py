from google.appengine.api import users


openid_providers = {
    'Google'   : 'https://www.google.com/accounts/o8/id',
    #'Yahoo'    : 'yahoo.com',
    #'MySpace'  : 'myspace.com',
    #'AOL'      : 'aol.com',
    #'MyOpenID' : 'myopenid.com'
    #'Steam'     : 'http://steamcommunity.com/openid'
    # add more here
}

def generate_login_urls(openid_providers=openid_providers, dest_url='/'):
    openid_logins = []

    for name, uri in openid_providers.items():

        login_url = users.create_login_url(federated_identity=uri, dest_url=dest_url)
    
        openid_logins.append([name, login_url])
        
    return openid_logins
    
def generate_login_google_only( dest_url='/'):
    openid_logins = []

    login_url = users.create_login_url(federated_identity='https://www.google.com/accounts/o8/id', dest_url=dest_url)
    
    openid_logins.append(['Google', login_url])
        
    return openid_logins
