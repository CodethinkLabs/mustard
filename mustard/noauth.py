# Copyright (C) 2012-2013 Codethink Limited


import mustard


class Authenticator(mustard.auth.Authenticator):

    def __init__(self, app, settings):
        mustard.auth.Authenticator.__init__(self, app, settings)

    def check_auth(self, username, password):
        return True
