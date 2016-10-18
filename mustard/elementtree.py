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


import os
import os.path

import mustard
import sys

import logging

try:
    from typing import Any, Sequence, List
except ImportError:
    pass

class ElementTree(object):
    def __init__(self, raw_tree):
        print("Initialize tree")
        self.raw_tree = raw_tree
        self.state = raw_tree.state
        self.element_factory = mustard.elementfactory.ElementFactory()
        self.elements = {} # type: dict[str, mustard.elementFactory.Element]

        self.project = mustard.project.Project({}) # type: mustard.project.Project
        self.project.tree = self 

        print("Performing initial load with no path")
        self._load_node('', self.raw_tree.data)
        self._resolve_project()
        self._resolve_links()

    def _load_element(self, path, node):
        # type: (ElementTree, str, dict) -> None
        print("Loading element: %s"%path)
        element = self.element_factory.create(node, self.state.app.base_url)
        element.title = element.title or os.path.basename(path)
        element.tree = self
        element.name = path
        self.elements[path] = element

    def _resolve_project(self):
        # Type: (ElementTree) -> None
        projects = [(x, y) for x, y in self.find_all(kind='project')]
        if len(projects) == 0:
            raise mustard.MustardError('No project defined')
        elif len(projects) > 1:
            raise mustard.MustardError('%s project nodes found: %r' %
                                       (len(projects),
                                        [x for x, y in projects]))
        else:
            self.project = projects[0][1]

    def _resolve_links(self):
        self._resolve_auto_parents()
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

    def _resolve_component_links(self):
        for path, element in self.find_all(kind='component'):
            self._resolve_parent_component(path, element)
            self._resolve_mapped_here(path, element)
            self._resolve_tags(path, element)

    def _resolve_integration_strategy_links(self):
        for path, element in self.find_all(kind='integration-strategy'):
            self._resolve_parent_component(path, element)
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
            self._resolve_parent_work_item(path, element)
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
            if element.kind == 'component':
                self.elements[ref].components[path] = element
            elif element.kind == 'interface':
                self.elements[ref].interfaces[path] = element
            elif element.kind == 'integration-strategy':
                if hasattr(self.elements[ref], 'integration_strategy') and \
                        self.elements[ref].integration_strategy[1] is not None:
                    raise mustard.MustardError(
                        '%s is attempting to be the integration strategy for '
                        '%s which already has %s as its integration strategy.'
                        % (path, ref,
                            self.elements[ref].integration_strategy[0]))
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

    def _resolve_parent_work_item(self, path, item):
        ref = item.parent[0]
        if ref in self.elements:
            item.parent = (ref, self.elements[ref])
            if item.parent[1].kind != 'work-item':
                raise mustard.MustardError(
                    '%s is referencing %s (kind: %s) as its parent, but '
                    'work items may only have work items as their parent' % (
                        path, ref, item.parent[1].kind))
            self.elements[ref].work_items[path] = item

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
            results[:] = [(p, e) for (p, e) in results if e.is_toplevel()]
        return mustard.sorting.sort_elements(results, kwargs)

    def yaml(self):
        return self.raw_tree.yaml()

class MustardTree(ElementTree):
    def _load_node(self, path, node):
        # type: (MustardTree, str, dict[str, Any]) -> None
        # node is the raw data from the input YAML
        print("_load_node: %s for node %s"%(path, node))
        if 'kind' in node:
            print(" - This is of kind %s"%node['kind'])
            self._load_element(path, node)
        children = [(x, y) for x, y in node.items()
                    if isinstance(y, dict)]
        for segment, child in children:
            self._load_node(os.path.join(path, segment), child)

class OpenControlTree(ElementTree):
    def _load_node(self, path, raw_tree_data):
        # type: (MustardTree, str, dict[str, Any]) -> None
        print("_load_node: %s for node %s"%(path, raw_tree_data))
        raw_tree_data['kind'] = "project"

        element = self.element_factory.create(raw_tree_data, self.state.app.base_url) # type: mustard.elementFactory.Element
        element.tree = self
        self.elements['project'] =  element
        for (k,v) in raw_tree_data['opencontrol'].items():
            print("Processing the field %s from the project file"%k);
            if k.lower() == 'dependencies':
                self._load_dependencies(v)
            elif k.lower() == 'components':
                self._load_components(v)
            elif k.lower() == 'name':
                self.elements['project'].name = v

    def _make_element(self, raw_data, path):
        element = self.element_factory.create(raw_data,self.state.app.base_url)
        element.tree = self
        self.elements[path] = element

    def _load_dependent_standards(self, standard_list):
        # type: (Sequence[ dict[str,str]]) -> None
        for s in standard_list:
            url = s['url']
            revision = s['revision']
            print("At this point we should attempt a clone of %s:%s"%(url, revision))
            # This should be a new elementTree...

            # Create an example of the kind of data we want in requirements:
            
            self._make_element({'kind': 'requirement', 'name': 'req-ex-1', 'title': 'Example requirement 1'}, 'req1')
            self._make_element({'kind': 'requirement', 'name': 'req-ex-2', 'title': 'Example requirement 2'}, 'req1/req2')

    def _load_dependent_certifications(self, cert_list):
        pass
    def _load_dependent_systems(self, cert_list):
        pass
    
    def _load_dependencies(self, deps):
        # type: (dict[str, Any]) -> None
        for (k,v) in deps.items():
            print("Processing the dependency %s"%k)
            if k.lower() == 'standards':
                self._load_dependent_standards(v)
            elif k.lower() == 'certifications':
                self._load_dependent_certifications(v)
            elif k.lower() == 'systems':
                self._load_dependent_systems(v)
            else:
                print("Unidentified dependency type: %s?"%k)
    def _load_components(self, deps):
        pass
        

class Cache(object):

    def __init__(self, raw_tree_cache):
        self.raw_tree_cache = raw_tree_cache
        self.trees = {}

    def get(self, state):
        # type: (Cache, object) -> object
        print("cache::get")
        if not state in self.trees:
            raw_tree = self.raw_tree_cache.get(state)
            print("Creating an elementTree from the raw tree...")
            if 'opencontrol' in raw_tree.data:
                self.trees[state] = OpenControlTree(raw_tree)
            else:
                self.trees[state] = MustardTree(raw_tree)
        return self.trees[state]
