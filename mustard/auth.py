# Copyright (c) 2013 Codethink Limited


import bottle

from functools import wraps


class Authenticator(object):

    def __init__(self, app, settings):
        self.app = app
        self.auth_server = settings['auth-server']
        self.auth_user = settings['auth-user']
        self.auth_password = settings['auth-password']
        self.project = settings['project-code']

    def authenticate(self):
        return bottle.HTTPResponse('Login Required', 401, {
            'WWW-Authenticate': 'Basic realm="Login Required"'
            })

    def protected(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            if bottle.request.auth:
                username, password = bottle.request.auth
            else:
                username, password = (None, None)
            if not self.check_auth(username, password):
                return self.authenticate()
            return func(*args, **kwargs)
        return decorated
