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
        if self.sha1 == 'UNCOMMITTED':
            sha1s = ['UNCOMMITTED'] + self.repository.history(None)
        else:
            sha1s = self.repository.history(self.sha1)
        return [self.cache.get(x) for x in sha1s]

    def diff_against(self, other):
        return self.repository.diff(other.sha1, self.sha1)


class UncommittedState(State):

    def __init__(self, app, cache, repository):
        State.__init__(self, app, cache, repository)

        self.identifier = 'UNCOMMITTED'
        self.sha1 = 'UNCOMMITTED'
        self.title = 'UNCOMMITTED'
        self.diff = self.repository.diff(None)

    def filenames(self):
        return self._list_files()

    def _list_files(self):
        # collect all elements from the project dir
        for root, dirs, files in os.walk(self.repository.dirname):
            # do not recurse into hidden subdirectories
            dirs[:] = [x for x in dirs if not x.startswith('.')]

            # remove the /files directory from the list as we don't
            # want to include YAML files in that directory
            if os.path.samefile(root, self.repository.dirname):
                if 'files' in dirs:
                    dirs.remove('files')

            # skip all non-YAML and hidden files
            files[:] = [x for x in files
                        if x.endswith('.yaml') and not x.startswith('.')]

            # load all YAML files into the element tree
            for filename in files:
                yield os.path.relpath(os.path.join(root, filename),
                                      self.repository.dirname)

    def read(self, filename):
        return open(os.path.join(self.repository.dirname, filename)).read()


class CommittedState(State):

    def __init__(self, app, cache, repository, ref, sha1):
        State.__init__(self, app, cache, repository)

        self.identifier = ref
        self.sha1 = sha1

        commit = self.repository.commit(self.sha1)

        self.author = commit.author.name
        self.author_email = commit.author.email
        self.date = commit.author.time
        self.title = commit.message.splitlines()[0]
        self.body = '\n'.join(commit.message.splitlines()[1:])

        if commit.parents:
            try:
                self.diff = commit.parents[0].tree.diff(commit.tree).patch
            except AttributeError:
                self.diff = commit.parents[0].tree.diff_to_tree(
                    commit.tree).patch
            self.left = commit.parents[0].hex
            if len(commit.parents) > 1:
                self.right = commit.parents[1].hex
        else:
            self.diff = ''
            self.left = None
            self.right = None

        self._cached_filenames = []

    def filenames(self):
        if not self._cached_filenames:
            self._cached_filenames = list(self._list_files())
        return self._cached_filenames

    def _list_files(self):
        tree = self.repository.list_tree(self.sha1)
        for filename in tree:
            # ignore files in /files because we do not want to include
            # YAML files in that directory
            if not filename.startswith('files/') \
                    and not filename.startswith('.') \
                    and filename.endswith('.yaml'):
                yield filename

    def read(self, filename):
        return self.repository.cat_file(self.sha1, filename)


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
                # resolve the (potentially symbolic) ref into a SHA1
                sha1 = self.repository.resolve_ref(ref)

                # we cache content for a combination of commit SHA1
                # and list of refs in the repository; this means the
                # cache is invalidated when either our ref moves on
                # or other refs (e.g. tags or branches) are added or
                # removed
                key = (sha1,
                       tuple(self.repository.tags()),
                       tuple(self.repository.branches()))

                if not key in self.states:
                    print '%s not in cache' % sha1
                    self.states[key] = CommittedState(
                        self.app, self, self.repository, ref, sha1)
                print '%s now cached' % sha1
                return self.states[key]
            except cliapp.AppException, err:
                raise InvalidStateError(ref)
