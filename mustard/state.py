# Copyright (C) 2012 Codethink Limited


import cliapp
import os


class InvalidStateError(cliapp.AppException):
    
    def __init__(self, ref):
        cliapp.AppException.__init__(
                self, 'Failed to resolve state "%s"' % ref)


class State(object):

    def __init__(self, app, cache, repository):
        self.app = app
        self.cache = cache
        self.repository = repository
        self.title = None
        self.body = None
        self.author = None
        self.author_email = None
        self.left = None
        self.right = None
        self.diff = None
        self.date = None

    def history(self):
        raise NotImplementedError

    def _history_states(self, ref):
        if ref == 'UNCOMMITTED':
            sha1s = self.app.runcmd(
                    ['git', 'log', '--first-parent', '--format=%H %P'],
                    cwd=self.repository.dirname)
        else:
            sha1s = self.app.runcmd(
                    ['git', 'log', '--first-parent', '--format=%H %P', ref],
                    cwd=self.repository.dirname)
        
        states = [self] if ref == 'UNCOMMITTED' else []
        for line in sha1s.splitlines():
            parts = line.split()
            states.append(self.cache.get(parts[0]))
        return states

    def diff_against(self, other):
        return self.app.runcmd(
                ['git', 'diff', '%s..%s' % (other.sha1, self.sha1)],
                cwd=self.repository.dirname).strip()

class UncommittedState(State):

    def __init__(self, app, cache, repository):
        State.__init__(self, app, cache, repository)

        self.identifier = 'UNCOMMITTED'
        self.sha1 = 'UNCOMMITTED'
        self.title = 'UNCOMMITTED'
        self.diff = self.app.runcmd(
                ['git', 'diff'], cwd=self.repository.dirname).strip()

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

    def history(self):
        return self._history_states(self.identifier)

class CommittedState(State):

    def __init__(self, app, cache, repository, ref, sha1):
        State.__init__(self, app, cache, repository)

        self.identifier = ref
        self.sha1 = sha1

        fmt = '%an\n%ae\n%ad\n%P\n%s\n%b\n{{DIFF}}'
        log = self.app.runcmd(
                ['git', 'show', '--format=%s' % fmt, self.sha1],
                cwd=self.repository.dirname).splitlines()

        self.author = log[0].strip()
        self.author_email = log[1].strip()
        self.date = log[2].strip()
        self.title = log[4].strip()
        
        parents = log[3].split()
        if len(parents) > 0:
            self.left = parents[0]
        if len(parents) > 1:
            self.right = parents[1]

        self.body = []
        self.diff = []
        diff_started = False
        for line in log[5:]:
            if not diff_started:
                if line.startswith('{{DIFF}}'):
                    diff_started = True
                else:
                    self.body.append(line)
            else:
                self.diff.append(line)
        
        self.body = '\n'.join(self.body).strip()
        self.diff = '\n'.join(self.diff).strip()

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

    def history(self):
        return self._history_states(self.sha1)


class Cache(object):

    def __init__(self, app, repository):
        self.app = app
        self.repository = repository
        self.states = {}

    def get(self, ref):
        if ref == 'UNCOMMITTED':
            if not ref in self.states:
                self.states[ref] = UncommittedState(
                        self.app, self, self.repository)
            return self.states[ref]
        else:
            try:
                sha1 = self.resolve_ref(ref)
                if not sha1 in self.states:
                    self.states[sha1] = CommittedState(
                            self.app, self, self.repository, ref, sha1)
                return self.states[sha1]
            except cliapp.AppException, err:
                raise InvalidStateError(ref)

    def resolve_ref(self, ref):
        rev = self.app.runcmd(['git', 'rev-list', '-n1', ref],
                              cwd=self.repository.dirname)
        return rev.split()[0]
