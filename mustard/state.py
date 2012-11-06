# Copyright (C) 2012 Codethink Limited


import os


class State(object):

    def __init__(self, app, dirname, identifier):
        self.app = app
        self.dirname = dirname
        self.identifier = identifier

    def list_tree(self):
        if self.identifier == 'UNCOMMITTED':
            return self._list_uncommitted_tree()
        else:
            return self._list_commit_tree()

    def read(self, filename):
        if self.identifier == 'UNCOMMITTED':
            return self._read_uncommitted_file(filename)
        else:
            return self._read_commit_file(filename)

    def _list_uncommitted_tree(self):
        # collect all elements from the project dir
        for root, dirs, files in os.walk(self.dirname):
            # do not recurse into hidden subdirectories
            dirs[:] = [x for x in dirs if not x.startswith('.')]

            # skip all non-YAML and hidden files
            files[:] = [x for x in files
                        if x.endswith('.yaml') and not x.startswith('.')]

            # load all YAML files into the element tree
            for filename in files:
                yield os.path.relpath(os.path.join(root, filename),
                                      self.dirname)

    def _read_uncommitted_file(self, filename):
        return open(os.path.join(self.dirname, filename)).read()

    def _list_commit_tree(self):
        tree = self.app.runcmd(['git', 'ls-tree', '-r', self.identifier],
                               cwd=self.dirname)
        for line in tree.splitlines():
            filename = line.split()[3]
            if filename.endswith('.yaml') and not filename.startswith('.'):
                yield filename

    def _read_commit_file(self, filename):
        blob = '%s:%s' % (self.identifier, filename)
        return self.app.runcmd(['git', 'cat-file', 'blob', blob],
                               cwd=self.dirname)
