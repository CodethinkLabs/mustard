# Copyright (C) 2012 Codethink Limited


import cliapp
import os
import yaml

import mustard


class NonDictElementError(cliapp.AppException):

    def __init__(self, node):
        cliapp.AppException.__init__(
                self, 'Non-dictionary found: %s' % node)


class Tree(object):

    def __init__(self, raw_tree):
        self.raw_tree = raw_tree
        self.element_factory = mustard.elementfactory.ElementFactory()
        self.elements = {}

        self._load_node('', self.raw_tree.data)

        # TODO link all elements together

    def _load_node(self, path, node):
        if not isinstance(node, dict):
            raise NonDictElementError(node)
        else:
            if 'kind' in node:
                element = self._load_element(path, node)

            children = [(x,y) for x,y in node.iteritems()
                        if isinstance(y, dict)]
            for segment, child in children:
                self._load_node(os.path.join(path, segment), child)
            
    def _load_element(self, path, node):
        print 'load element: %s' % path
        self.elements[path] = self.element_factory.create(node)

    def yaml(self):
        return self.raw_tree.yaml()


class Cache(object):

    def __init__(self, raw_tree_cache):
        self.raw_tree_cache = raw_tree_cache
        self.trees = {}

    def get(self, state):
        if not state in self.trees:
            raw_tree = self.raw_tree_cache.get(state)
            self.trees[state] = Tree(raw_tree)
        return self.trees[state]
