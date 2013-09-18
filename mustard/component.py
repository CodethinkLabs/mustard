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


import markdown

import mustard


class Component(mustard.elementfactory.Element):

    def __init__(self, data):
        mustard.elementfactory.Element.__init__(self, data)

        self.interfaces = {}
        self.verificationcriteria = {}

        self.components = {}
        self.integration_strategy = (None, None)
        self.toplevel = data.get('toplevel', False)

        self.mapped_here = {}
        for ref in data.get('mapped-here', []):
            self.mapped_here[ref] = None

    def get_children(self):
        children = []
        for path, item in self.work_items.iteritems():
            if item:
                children.append((path, item))
        for path, component in self.components.iteritems():
            if component:
                children.append((path, component))
        for path, interface in self.interfaces.iteritems():
            if interface:
                children.append((path, interface))
        for path, criterion in self.verificationcriteria.iteritems():
            if criterion:
                children.append((path, criterion))
        if self.integration_strategy[1]:
            children.append(self.integration_strategy)
        return children

    def sort_subcomponents(self, **kwargs):
        return mustard.sorting.sort_elements(self.components.items(), kwargs)
