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
        if not ref:
            ref = self.repo.head.hex
        commit = self.commit(ref)
        while commit is not None:
            refs.append(commit.hex)
            if commit.parents:
                commit = commit.parents[0]
            else:
                commit = None
        return refs
    
    def diff(self, ref1=None, ref2=None):
        if ref1 and ref2:
            commit1 = self.commit(ref1)
            commit2 = self.commit(ref2)
            tree1 = commit1.tree
            tree2 = commit2.tree
            return tree1.diff(tree2).patch
        else:
            return self.repo.head.tree.diff().patch

    def commit(self, ref):
        sha1 = self.resolve_ref(ref)
        commit_or_tag = self.repo[sha1]
        if type(commit_or_tag) == pygit2.Tag:
            commit_or_tag = self.repo[commit_or_tag.target]
        return commit_or_tag

    def list_tree(self, ref):
        sha1 = self.resolve_ref(ref)
        queue = collections.deque()
        queue.append((self.commit(sha1).tree, ''))
        while queue:
            (tree, path) = queue.popleft()
            for entry in tree:
                if entry.filemode == 040000:
                    subtree = self.repo[entry.oid]
                    queue.append((subtree, os.path.join(path, entry.name)))
                else:
                    yield os.path.join(path, entry.name)

    def cat_file(self, ref, filename):
        commit = self.commit(ref)
        entry = commit.tree[filename]
        blob = self.repo[entry.oid]
        return blob.data

    def resolve_ref(self, ref):
        ref = ref.replace(':', '/')
        return self.repo.revparse_single(ref).hex
