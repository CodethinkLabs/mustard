# Copyright (C) 2012 Codethink Limited


import collections
import os

import mustard


class Trie(object):
    
    def __init__(self):
        self.parent = None
        self.children = {}

    def split(self, path):
        return [x for x in path.split('/') if len(x) > 0]

    def insert(self, path, node):
        segments = self.split(path)
        self._insert(path, segments, node)

    def _insert(self, path, segments, node):
        if len(segments) == 0:
            raise cliapp.AppException('Cannot replace \"/\"')
        elif len(segments) == 1:
            if segments[0] in self.children:
                raise cliapp.AppException('Element \"%s\" already exists' %
                                          path)
            else:
                self.children[segments[0]] = node
                self._propagate_descendant(path, node)
        else:
            if segments[0] in self.children:
                child = self.children[segments[0]]
            else:
                child = Trie()
                child.parent = self
                self.children[segments[0]] = child
            child._insert(path, segments[1:], node)

    def _propagate_descendant(self, path, node):
        if isinstance(node, mustard.requirement.Requirement):
            self._propagate_requirement(path, node)
        elif isinstance(node, mustard.tag.Tag):
            self._propagate_tag(path, node)
        if self.parent:
            self.parent._propagate_descendant(path, node)

    def _propagate_requirement(self, path, requirement):
        pass

    def _propagate_tag(self, path, tag):
        pass

    def lookup(self, path):
        segments = self.split(path)
        self._lookup(segments)

    def _lookup(self, segments):
        if len(segments) == 0:
            return self
        else:
            if segments[0] in self.children:
                if len(segments) == 1:
                    return self.children[segments[0]]
                else:
                    child = self.children[segments[0]]
                    return child._lookup(segments[1:])
            else:
                return None
