# Copyright (C) 2012 Codethink Limited


import cliapp
import pprint
import StringIO

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
        errors = []
        for filename in self.state.filenames():
            content = self.state.read(filename)
            io = StringIO.StringIO(content)
            setattr(io, 'name', filename)
            try:
                data = load_yaml(io, filename.replace('.yaml', ''))
                self._insert_raw(filename.replace('.yaml', ''), data)
            except Exception, error:
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
