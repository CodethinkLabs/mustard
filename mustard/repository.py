# Copyright (C) 2012 Codethink Limited


import cliapp
import collections
import os
import pygit2


class Repository(object):

    def __init__(self, app, dirname):
        self.app = app
        self.dirname = dirname
        self.repo = pygit2.Repository(self.dirname)

        self.checked_out = True if self.repo.workdir else False
    
    def history(self, ref):
        refs = []
        if ref:
            sha1 = self.resolve_ref(ref)
        else:
            sha1 = self.repo.head.hex
        for commit in self.repo.walk(sha1, pygit2.GIT_SORT_TIME):
            refs.append(commit.hex)
        return refs
    
    def diff(self, ref1=None, ref2=None):
        if ref1 and ref2:
            sha1 = self.resolve_ref(ref1)
            sha2 = self.resolve_ref(ref2)
            commit1 = self.repo[sha1]
            commit2 = self.repo[sha2]
            tree1 = commit1.tree
            tree2 = commit2.tree
            return tree1.diff(tree2).patch
        else:
            return self.repo.head.tree.diff().patch

    def commit(self, ref):
        sha1 = self.resolve_ref(ref)
        return self.repo[sha1]

    def list_tree(self, ref):
        sha1 = self.resolve_ref(ref)
        queue = collections.deque()
        queue.append((self.repo[sha1].tree, ''))
        while queue:
            (tree, path) = queue.popleft()
            for entry in tree:
                if entry.filemode == 040000:
                    subtree = self.repo[entry.oid]
                    queue.append((subtree, os.path.join(path, entry.name)))
                else:
                    yield os.path.join(path, entry.name)

    def cat_file(self, ref, filename):
        sha1 = self.resolve_ref(ref)
        commit = self.repo[sha1]
        entry = commit.tree[filename]
        blob = self.repo[entry.oid]
        return blob.data

    def resolve_ref(self, ref):
        ref = ref.replace(':', '/')
        return self.repo.revparse_single(ref).hex
