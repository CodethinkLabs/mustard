# Copyright (C) 2012 Codethink Limited


import collections
import os

import mustard


class Trie(object):
    
    def __init__(self):
        self._parent = None
        self._children = {}

    def split(self, path):
        return [x for x in path.split('/') if len(x) > 0]

    def insert(self, path, node):
        segments = self.split(path)
        self._insert(path, segments, node)

    def _insert(self, path, segments, node):
        if len(segments) == 0:
            raise cliapp.AppException('Cannot replace \"/\"')
        elif len(segments) == 1:
            if segments[0] in self._children:
                raise cliapp.AppException('Element \"%s\" already exists' %
                                          path)
            else:
                node._parent = self
                self._children[segments[0]] = node
                self._propagate_descendant(path, node)
        else:
            if segments[0] in self._children:
                child = self._children[segments[0]]
            else:
                child = Trie()
                child._parent = self
                self._children[segments[0]] = child
            child._insert(path, segments[1:], node)

    def _propagate_descendant(self, path, node):
        if node.kind == 'requirement':
            self._propagate_requirement(path, node)
        elif node.kind == 'tag':
            self._propagate_tag(path, node)
        elif node.kind == 'architecture':
            self._propagate_architecture(path, node)
        elif node.kind == 'component':
            self._propagate_component(path, node)
        elif node.kind == 'work-item':
            self._propagate_work_item(path, node)
        elif node.kind == 'interface':
            self._propagate_interface(path, node)
        if self._parent:
            self._parent._propagate_descendant(path, node)

    def _propagate_requirement(self, path, requirement):
        pass

    def _propagate_tag(self, path, tag):
        pass

    def _propagate_architecture(self, path, architecture):
        pass

    def _propagate_component(self, path, component):
        pass

    def _propagate_work_item(self, path, item):
        pass

    def _propagate_interface(self, path, interface):
        pass

    def lookup(self, path):
        segments = self.split(path)
        self._lookup(segments)

    def _lookup(self, segments):
        if len(segments) == 0:
            return self
        else:
            if segments[0] in self._children:
                if len(segments) == 1:
                    return self._children[segments[0]]
                else:
                    child = self._children[segments[0]]
                    return child._lookup(segments[1:])
            else:
                return None
