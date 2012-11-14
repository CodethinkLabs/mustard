# Copyright (C) 2012 Codethink Limited


import cliapp
import os
import yaml

from itertools import groupby

import mustard


class NonDictElementError(cliapp.AppException):

    def __init__(self, node):
        cliapp.AppException.__init__(
                self, 'Non-dictionary found: %s' % node)


class Tree(object):

    def __init__(self, raw_tree):
        self.raw_tree = raw_tree
        self.state = raw_tree.state
        self.element_factory = mustard.elementfactory.ElementFactory()
        self.elements = {}

        self.project = mustard.project.Project({})
        self.project.tree = self

        self._load_node('', self.raw_tree.data)
        self._resolve_project()
        self._resolve_links()

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
        element = self.element_factory.create(node)
        element.title = element.title or os.path.basename(path)
        element.tree = self
        self.elements[path] = element

    def _resolve_project(self):
        projects = [(x,y) for x,y in self.find_all(kind='project')]
        if projects:
            self.project = projects[0][1]

    def _resolve_links(self):
        self._resolve_architecture_links()
        self._resolve_component_links()
        self._resolve_integration_strategy_links()
        self._resolve_interface_links()
        self._resolve_requirement_links()
        self._resolve_tag_links()
        self._resolve_test_links()
        self._resolve_work_item_links()

    def _resolve_architecture_links(self):
        for path, element in self.find_all(kind='architecture'):
            self._resolve_parent_component(path, element)
            self._resolve_mapped_here(path, element)
            self._resolve_tags(path, element)

    def _resolve_component_links(self):
        for path, element in self.find_all(kind='component'):
            self._resolve_parent_architecture(path, element)
            self._resolve_mapped_here(path, element)
            self._resolve_tags(path, element)
    
    def _resolve_integration_strategy_links(self):
        for path, element in self.find_all(kind='integration-strategy'):
            self._resolve_parent_architecture(path, element)
            self._resolve_mapped_here(path, element)
            self._resolve_tags(path, element)
    
    def _resolve_interface_links(self):
        for path, element in self.find_all(kind='interface'):
            self._resolve_parent_component(path, element)
            self._resolve_mapped_here(path, element)
            self._resolve_tags(path, element)
    
    def _resolve_requirement_links(self):
        for path, element in self.find_all(kind='requirement'):
            self._resolve_parent_requirement(path, element)
            self._resolve_tags(path, element)
    
    def _resolve_tag_links(self):
        pass

    def _resolve_test_links(self):
        for path, element in self.find_all(kind='test'):
            self._resolve_parents(path, element)
            self._resolve_tags(path, element)

    def _resolve_work_item_links(self):
        for path, element in self.find_all(kind='work-item'):
            self._resolve_parents(path, element)
            self._resolve_tags(path, element)
    
    def _resolve_tags(self, path, element):
        for ref in element.tags.iterkeys():
            if ref in self.elements:
                element.tags[ref] = self.elements[ref]
                self.elements[ref].tagged[path] = element

    def _resolve_parent_component(self, path, element):
        ref = element.parent[0]
        if ref in self.elements:
            if element.kind == 'architecture':
                self.elements[ref].architecture = (path, element)
            elif element.kind == 'interface':
                self.elements[ref].interfaces[path] = element
            element.parent = (ref, self.elements[ref])

    def _resolve_parent_architecture(self, path, element):
        ref = element.parent[0]
        if ref in self.elements:
            if element.kind == 'component':
                self.elements[ref].components[path] = element
            elif element.kind == 'integration-strategy':
                self.elements[ref].integration_strategy = (path, element)
            element.parent = (ref, self.elements[ref])

    def _resolve_parent_requirement(self, path, requirement):
        ref = requirement.parent[0]
        if ref in self.elements:
            requirement.parent = (ref, self.elements[ref])
            self.elements[ref].subrequirements[path] = requirement

    def _resolve_parents(self, path, element):
        for ref in element.parents.iterkeys():
            if ref in self.elements:
                if element.kind == 'test':
                    if self.elements[ref].kind == 'requirement':
                        self.elements[ref].mapped_to[path] = element
                    else:
                        self.elements[ref].tests[path] = element
                elif element.kind == 'work-item':
                    if self.elements[ref].kind == 'requirement':
                        self.elements[ref].mapped_to[path] = element
                    else:
                        self.elements[ref].work_items[path] = element
                element.parents[ref] = self.elements[ref]

    def _resolve_mapped_here(self, path, element):
        for ref in element.mapped_here:
            if ref in self.elements:
                element.mapped_here[ref] = self.elements[ref]
                self.elements[ref].mapped_to[path] = element

    def find_all(self, **kwargs):
        results = []

        for path, element in self.elements.iteritems():
            if element.kind == kwargs.get('kind', element.kind):
                results.append((path, element))

        sort_by = kwargs.get('sort_by', None)
        reverse = kwargs.get('reverse', False)

        def compare_elements(pair1, pair2):
            def split_by_numbers(s):
                return [''.join(v) for _, v in groupby(s, lambda c: c.isdigit())]

            s1 = getattr(pair1[1], sort_by)
            s2 = getattr(pair2[1], sort_by)
            
            s1s = split_by_numbers(s1)
            s2s = split_by_numbers(s2)

            s1s.append('')
            s2s.append('')

            for left, right in zip(s1s, s2s):
                leftdigit = left.isdigit()
                rightdigit = right.isdigit()
                if leftdigit and rightdigit:
                    cmpres = cmp(int(left), int(right))
                    if cmpres != 0:
                        return cmpres
                if leftdigit:
                    return 1 if right == "" else -1
                if rightdigit:
                    return -1 if left == "" else 1
                cmpres = cmp(left, right)
                if cmpres != 0:
                    return cmpres
            return 0

        if sort_by:
            return sorted(results,
                          cmp=compare_elements,
                          reverse=reverse)
        else:
            return results

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
