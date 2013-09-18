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


import collections
import os
import pygit2


class Repository(object):

    def __init__(self, app, dirname):
        self.app = app
        self.dirname = dirname
        self.repo = pygit2.Repository(self.dirname)

        self.checked_out = True if self.repo.workdir else False

    def is_bare(self):
        return self.repo.config['core.bare']

    def tags(self):
        for ref in self.repo.listall_references():
            if ref.startswith('refs/tags/'):
                yield ref, self.escape_ref(ref.replace('refs/tags/', ''))

    def branches(self):
        for ref in self.repo.listall_references():
            if ref != 'refs/heads/admin' and ref.startswith('refs/heads/'):
                yield ref, self.escape_ref(ref.replace('refs/heads/', ''))

    def history(self, ref):
        refs = []
        if not ref:
            try:
                ref = self.repo.head.hex
            except AttributeError:
                ref = self.repo.head.get_object().oid.hex
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
            try:
                return self.repo.head.tree.diff().patch
            except AttributeError:
                try:
                    return self.repo.diff('HEAD').patch
                except pygit2.GitError:
                    return ''

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

    def escape_ref(self, ref):
        return ref.replace('/', ':')

    def unescape_ref(self, ref):
        return ref.replace(':', '/')

    def resolve_ref(self, ref):
        ref = self.unescape_ref(ref)
        return self.repo.revparse_single(ref).hex
