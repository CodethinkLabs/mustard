# Copyright (C) 2012-2013 Codethink Limited


import yaml
import StringIO

import mustard


class Authenticator(mustard.auth.Authenticator):

    def __init__(self, app, settings, repository):
        mustard.auth.Authenticator.__init__(self, app, settings)
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
