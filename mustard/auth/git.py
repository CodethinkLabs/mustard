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


import yaml
import StringIO

import mustard


class Authenticator(mustard.authenticator.Authenticator):

    def __init__(self, app, settings, repository):
        mustard.authenticator.Authenticator.__init__(
            self, app, settings, repository)

    def check_auth(self, username, password):
        try:
            data = self.repository.cat_file('admin', 'acl.yaml')
        except KeyError:
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
