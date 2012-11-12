# Copyright (C) 2012 Codethink Limited


import cliapp
import os


class InvalidStateError(cliapp.AppException):
    
    def __init__(self, ref):
        cliapp.AppException.__init__(
                self, 'Failed to resolve state "%s"' % ref)


class State(object):

    def __init__(self, app, repository):
        self.app = app
        self.repository = repository


class UncommittedState(object):

    def __init__(self, repository):
        self.repository = repository
        self.identifier = 'UNCOMMITTED'

    def filenames(self):
        return self._list_files()

    def _list_files(self):
        # collect all elements from the project dir
        for root, dirs, files in os.walk(self.repository.dirname):
            # do not recurse into hidden subdirectories
            dirs[:] = [x for x in dirs if not x.startswith('.')]

            # skip all non-YAML and hidden files
            files[:] = [x for x in files
                        if x.endswith('.yaml') and not x.startswith('.')]

            # load all YAML files into the element tree
            for filename in files:
                yield os.path.relpath(os.path.join(root, filename),
                                      self.repository.dirname)
    
    def read(self, filename):
        return open(os.path.join(self.repository.dirname, filename)).read()


class CommittedState(object):

    def __init__(self, app, repository, ref, sha1):
        self.app = app
        self.repository = repository
        self.identifier = ref
        self.sha1 = sha1
        self._cached_filenames = []

    def filenames(self):
        if not self._cached_filenames:
            self._cached_filenames = list(self._list_files())
        return self._cached_filenames

    def _list_files(self):
        tree = self.app.runcmd(['git', 'ls-tree', '-r', self.sha1],
                               cwd=self.repository.dirname)
        for line in tree.splitlines():
            filename = line.split()[3]
            if not filename.startswith('.') and filename.endswith('.yaml'):
                yield filename

    def read(self, filename):
        blob = '%s:%s' % (self.sha1, filename)
        return self.app.runcmd(['git', 'cat-file', 'blob', blob],
                               cwd=self.repository.dirname)


class Cache(object):

    def __init__(self, app, repository):
        self.app = app
        self.repository = repository
        self.states = {}

    def get(self, ref):
        if ref == 'UNCOMMITTED':
            if not ref in self.states:
                self.states[ref] = UncommittedState(self.repository)
            return self.states[ref]
        else:
            try:
                sha1 = self.resolve_ref(ref)
                if not sha1 in self.states:
                    self.states[sha1] = CommittedState(
                            self.app, self.repository, ref, sha1)
                return self.states[sha1]
            except cliapp.AppException, err:
                raise InvalidStateError(ref)

    def resolve_ref(self, ref):
        rev = self.app.runcmd(['git', 'rev-list', '-n1', ref],
                              cwd=self.repository.dirname)
        return rev.split()[0]
