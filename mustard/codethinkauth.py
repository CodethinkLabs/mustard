# Copyright (C) 2013 Codethink Limited


import ctauth

import mustard


class Authenticator(mustard.auth.Authenticator):

    def __init__(self, app, settings):
        mustard.auth.Authenticator.__init__(self, app, settings)

    def check_auth(self, username, password):
        user = ctauth.user.User(username, password)
        context = ctauth.context.Context(self.project, 'mustard')

        try:
            with ctauth.auth.Auth(
                    self.auth_server,
                    self.auth_user,
                    self.auth_password) as server:
                permissions = server.authenticate(user, context)
                if permissions.can_read() or permissions.is_customer():
                    return True
                else:
                    return False
        except Exception, err:
            print repr(err)
            return False
