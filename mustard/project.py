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


import mustard


valid_sort_by = set(["title", "location", "name"])


class Project(mustard.elementfactory.Element):

    def __init__(self, data):
        mustard.elementfactory.Element.__init__(self, data)
        self.kind = 'project'
        self.copyright = data.get('copyright', None)
        self.predefined_filters = data.get('predefined-filters', [])
        self.sort_by = data.get('sort-by', 'location')
        if self.sort_by not in valid_sort_by:
            raise mustard.MustardError(
                "Unknown sort-by (%s) in project node. "
                "Possible sort-by options are: %s" % (
                    self.sort_by, ", ".join(valid_sort_by)))
