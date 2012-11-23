# Copyright (C) 2012 Codethink Limited


import bottle
import yaml
import StringIO

from functools import wraps


class Authenticator(object):

    def __init__(self, repository):
        self.repository = repository

    def check_auth(self, username, password):
        try:
            data = self.repository.cat_file('admin', 'acl.yaml')
        except KeyError, err:
            return False
        io = StringIO.StringIO(data)
        acl = yaml.load(io)
        
        if 'users' in acl:
            if username in acl['users'] and acl['users'][username] == password:
                return True
            else:
                return False
        else:
            return False

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
