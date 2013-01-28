# Copyright (C) 2012 Codethink Limited


import cliapp
import os
import os.path
import yaml

import mustard


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
        element.name = path
        self.elements[path] = element
        return element

    def _resolve_project(self):
        projects = [(x,y) for x,y in self.find_all(kind='project')]
        if len(projects) == 0:
            raise mustard.MustardError('No project defined')
        elif len(projects) > 1:
            raise mustard.MustardError('%s project nodes found: %r' % 
                                       (len(projects),
                                        [x for x,y in projects]))
        else:
            self.project = projects[0][1]

    def _resolve_links(self):
        self._resolve_auto_parents()
        self._resolve_architecture_links()
        self._resolve_component_links()
        self._resolve_integration_strategy_links()
        self._resolve_interface_links()
        self._resolve_requirement_links()
        self._resolve_tag_links()
        self._resolve_verification_criterion_links()
        self._resolve_work_item_links()

    def _resolve_auto_parents(self):
        for path, element in self.elements.items():
            if element.parent[0] is not None:
                continue
            parent_path = os.path.dirname(path)
            if parent_path in self.elements:
                element.parent = (parent_path, None)


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

    def _resolve_verification_criterion_links(self):
        for path, element in self.find_all(kind='verification-criterion'):
            self._resolve_criterion_parent(path, element)
            self._resolve_mapped_here(path, element)
            self._resolve_tags(path, element)

    def _resolve_work_item_links(self):
        for path, element in self.find_all(kind='work-item'):
            self._resolve_parents(path, element)
            self._resolve_mapped_here(path, element)
            self._resolve_tags(path, element)
    
    def _resolve_tags(self, path, element):
        for ref in element.tags.iterkeys():
            if ref in self.elements:
                element.tags[ref] = self.elements[ref]
                self.elements[ref].tagged[path] = element

    def _resolve_criterion_parent(self, path, element):
        ref = element.parent[0]
        if ref in self.elements:
            if self.elements[ref].kind == 'requirement':
                self.elements[ref].mapped_to[path] = element
            else:
                if not hasattr(self.elements[ref],
                               'verificationcriteria'):
                    raise mustard.MustardError(
                        '%s incorrectly refers to %s (kind: %s) which '
                        'cannot have verification criteria' % (
                            path, ref, self.elements[ref].kind))
                self.elements[ref].verificationcriteria[path] = element
            element.parent = (ref, self.elements[ref])

    def _resolve_parent_component(self, path, element):
        ref = element.parent[0]
        if ref in self.elements:
            if self.elements[ref].kind != 'component':
                raise mustard.MustardError(
                    '%s (kind: %s) has %s (kind: %s) as a parent, but may '
                    'only be parented to a component.' % (
                        path, element.kind, ref, self.elements[ref].kind))
            if element.kind == 'architecture':
                self.elements[ref].architecture = (path, element)
            elif element.kind == 'interface':
                self.elements[ref].interfaces[path] = element
            element.parent = (ref, self.elements[ref])

    def _resolve_parent_architecture(self, path, element):
        ref = element.parent[0]
        if ref in self.elements:
            if self.elements[ref].kind != 'architecture':
                raise mustard.MustardError(
                    '%s (kind: %s) has %s (kind: %s) as a parent, but can '
                    'only be parented to an architecture.' % (
                        path, element.kind, ref, self.elements[ref].kind))
            if element.kind == 'component':
                self.elements[ref].components[path] = element
            elif element.kind == 'integration-strategy':
                if hasattr(self.elements[ref], 'integration_strategy') and \
                        self.elements[ref].integration_strategy[1] is not None:
                    raise mustard.MustardError(
                        '%s is attempting to be the integration strategy for '
                        '%s which already has %s as its integration strategy.'
                        % (path, ref, self.elements[ref].integration_strategy[0]))
                self.elements[ref].integration_strategy = (path, element)
            element.parent = (ref, self.elements[ref])

    def _resolve_parent_requirement(self, path, requirement):
        ref = requirement.parent[0]
        if ref in self.elements:
            requirement.parent = (ref, self.elements[ref])
            if requirement.parent[1].kind != 'requirement':
                raise mustard.MustardError(
                    '%s is listing %s (kind: %s) as its parent, but '
                    'requirements may only have requirements as parents' % (
                        path, ref, requirement.parent[1].kind))
            self.elements[ref].subrequirements[path] = requirement

    def _resolve_parents(self, path, element):
        for ref in element.parents.iterkeys():
            if ref in self.elements:
                if element.kind == 'work-item':
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
        if kwargs.get('top_level'):
	    results = [ (p,e) for (p,e) in results if e.parent == (None,None) ]
        return mustard.sorting.sort_elements(results, kwargs)

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
