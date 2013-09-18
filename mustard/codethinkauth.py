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


try:
    import ctauth
except:
    import sys
    sys.stderr.write('Warning: Failed to import python-ctauth.\n'
                     'The "codethink" authentication mechanism will '
                     'not be available\n')

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
                if server.authenticate(user):
                    permissions = server.authorise(user, context)
                    if permissions.can_read() or permissions.is_customer():
                        return True
                    else:
                        return False
        except Exception, err:
            print repr(err)
            return False
