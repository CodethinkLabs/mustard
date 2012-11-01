# Copyright (C) 2012 Codethink Limited


import cliapp

import mustard


class Project(mustard.elementfactory.Element):

    def __init__(self):
        mustard.elementfactory.Element.__init__(self, {})
        self.kind = 'project'
        self.elements = {}

    def _propagate_requirement(self, path, requirement):
        self.elements[path] = requirement

        self._resolve_tags(path, requirement)
        self._resolve_requirement(path, requirement)
        
        self._resolve_links(path, requirement)
        self._resolve_backlinks(path, requirement)

    def _propagate_tag(self, path, tag):
        self.elements[path] = tag

        for ref, element in self.elements.iteritems():
            if path in element.tags:
                element.tags[path] = tag
                tag.tagged[ref] = element
        
        self._resolve_links(path, tag)
        self._resolve_backlinks(path, tag)

    def _propagate_architecture(self, path, architecture):
        self.elements[path] = architecture
        
        self._resolve_tags(path, architecture)
        self._resolve_components(path, architecture)
        self._resolve_component(path, architecture)
        self._resolve_mapped_here(path, architecture)
        
        self._resolve_links(path, architecture)
        self._resolve_backlinks(path, architecture)

    def _propagate_component(self, path, component):
        self.elements[path] = component

        self._resolve_tags(path, component)
        self._resolve_parent_architecture(path, component)
        self._resolve_architecture(path, component)
        self._resolve_mapped_here(path, component)
        
        self._resolve_links(path, component)
        self._resolve_backlinks(path, component)

    def _propagate_work_item(self, path, item):
        self.elements[path] = item

        self._resolve_tags(path, item)
        
        self._resolve_links(path, item)
        self._resolve_backlinks(path, item)

    def _resolve_tags(self, path, element):
        for ref in element.tags.iterkeys():
            if ref in self.elements:
                element.tags[ref] = self.elements[ref]
                self.elements[ref].tagged[path] = element
            else:
                raise cliapp.AppException(
                    'Tag \"%s\" used by \"%s\" not found' % (ref, path))

    def _resolve_components(self, path, element):
        for ref, component in self.elements.iteritems():
            if component.kind == 'component':
                if component.parent_architecture == path:
                    component.parent_architecture = (path, element)
                    element.components[ref] = component

    def _resolve_component(self, path, element):
        if element.for_component in self.elements:
            element.for_component = (
                    element.for_component,
                    self.elements[element.for_component])
            element.for_component[1].architecture = (path, element)

    def _resolve_parent_architecture(self, path, element):
        if element.parent_architecture in self.elements:
            element.parent_architecture = (
                    element.parent_architecture,
                    self.elements[element.parent_architecture])
            element.parent_architecture[1].components[path] = element

    def _resolve_architecture(self, path, element):
        for ref, architecture in self.elements.iteritems():
            if architecture.kind == 'architecture':
                if architecture.for_component:
                    if architecture.for_component == path:
                        architecture.for_component = (path, element)
                        element.architecture = (ref, architecture)

    def _resolve_mapped_here(self, path, element):
        for ref in element.mapped_here:
            if ref in self.elements:
                element.mapped_here[ref] = self.elements[ref]
                self.elements[ref].mapped_to[path] = element

    def _resolve_requirement(self, path, requirement):
        for ref, element in self.elements.iteritems():
            if hasattr(element, 'mapped_here'):
                if path in element.mapped_here:
                    element.mapped_here[path] = requirement
                    requirement.mapped_to[ref] = element
            if hasattr(element, 'parent_requirements'):
                if path in element.parent_requirements:
                    element.parent_requirements[path] = requirement
                    requirement.sub_requirements[ref] = element
        for ref in requirement.parent_requirements.iterkeys():
            if ref in self.elements:
                requirement.parent_requirements[ref] = self.elements[ref]
                self.elements[ref].sub_requirements[path] = requirement

    def _resolve_links(self, path, element):
        for ref in element.links.iterkeys():
            if ref in self.elements:
                element.links[ref] = self.elements[ref]
                self.elements[ref].backlinks[path] = element

    def _resolve_backlinks(self, path, element):
        for ref, other in self.elements.iteritems():
            if path in other.links:
                other.links[path] = element
                element.backlinks[ref] = other

    def find(self, kind):
        for path, element in self.elements.iteritems():
            if element.kind == kind:
                yield path, element
