# Copyright (C) 2012-2013 Codethink Limited
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
