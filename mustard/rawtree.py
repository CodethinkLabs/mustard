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


import cliapp
import StringIO
import yaml

from mustard.util import load_yaml


class DuplicateElementError(cliapp.AppException):

    def __init__(self, path):
        cliapp.AppException.__init__(
            self, 'Duplicate element "%s" found' % path)


class LoadError(cliapp.AppException):

    def __init__(self, errors):
        message = 'Failed to load files:\n\n%s' % \
            '\n\n'.join([str(x) for x in errors])
        cliapp.AppException.__init__(self, message)


class Tree(object):

    def __init__(self, state):
        self.state = state
        self.data = {}
        self._load()

    def _load(self):
        filenames = self.state.filenames()

        print("Loading raw tree from the initial list of filenames: %s"%filenames)
        if 'opencontrol.yaml' in filenames:
            self._load_opencontrol_data()
            return

        errors = []
        for filename in filenames:
            content = self.state.read(filename)
            io = StringIO.StringIO(content)
            setattr(io, 'name', filename)
            try:
                data = load_yaml(io, filename.replace('.yaml', ''))
                path = filename.replace('.yaml', '')
                print("Loading raw tree from the file %s into the path %s"%(filename, path))
                self._insert_raw(path, data)
            except Exception as error:
                errors.append(error)
        if errors:
            raise LoadError(errors)

    def _load_opencontrol_data(self):
        errors = []
        filename = "opencontrol.yaml"
        content = self.state.read(filename)
        io = StringIO.StringIO(content)
        setattr(io, 'name', filename)
        try:
            data = load_yaml(io, filename.replace('.yaml', ''))
            path = filename.replace('.yaml', '')
            print("Loading raw tree from the file %s into the path %s"%(filename, path))
            self._insert_raw(path, data)
        except Exception as error:
            errors.append(error)
            
        if errors:
            raise LoadError(errors)

    def _insert_raw(self, path, data):
        segments = self._split(path)
        current = self.data
        while segments:
            segment = segments[0]
            segments[:] = segments[1:]

            if segments:
                if segment in current:
                    current = current[segment]
                else:
                    current[segment] = {}
                    current = current[segment]
            else:
                if segment in current:
                    raise DuplicateElementError(path)
                else:
                    current[segment] = data

    def _split(self, path):
        return [x for x in path.split('/') if x]

    def yaml(self):
        return yaml.dump(self.data, indent=4, width=72,
                         default_flow_style=False)


class Cache(object):

    def __init__(self):
        self.trees = {}

    def get(self, state):
        if not state in self.trees:
            self.trees[state] = Tree(state)
        return self.trees[state]
