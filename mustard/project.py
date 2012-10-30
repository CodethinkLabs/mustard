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

    def _propagate_tag(self, path, tag):
        self.elements[path] = tag

        for element in self.elements.itervalues():
            if path in element.tags:
                element.tags[path] = tag

    def _propagate_architecture(self, path, architecture):
        self.elements[path] = architecture
        
        self._resolve_tags(path, architecture)
        self._resolve_components(path, architecture)
        self._resolve_satisfies(path, architecture)

    def _propagate_component(self, path, component):
        self.elements[path] = component

        self._resolve_tags(path, component)
        self._resolve_architecture(path, component)
        self._resolve_satisfies(path, component)

    def _resolve_tags(self, path, element):
        for ref in element.tags.iterkeys():
            if ref in self.elements:
                element.tags[ref] = self.elements[ref]
            else:
                raise cliapp.AppException(
                    'Tag \"%s\" used by \"%s\" not found' % (ref, path))

    def _resolve_components(self, path, element):
        for ref, component in self.elements.iteritems():
            if component.kind == 'component':
                if component.architecture == path:
                    component.architecture = (path, element)
                    element.components[ref] = component

    def _resolve_architecture(self, path, element):
        if element.architecture in self.elements:
            element.architecture = (
                    element.architecture, self.elements[element.architecture])
            element.architecture[1].components[path] = element

    def _resolve_satisfies(self, path, element):
        for ref in element.satisfies:
            if ref in self.elements:
                element.satisfies[ref] = self.elements[ref]

    def _resolve_requirement(self, path, requirement):
        for ref, element in self.elements.iteritems():
            if hasattr(element, 'satisfies'):
                if path in element.satisfies:
                    element.satisfies[path] = requirement
                    requirement.satisfied_by[ref] = element

    def find(self, kind):
        for path, element in self.elements.iteritems():
            if element.kind == kind:
                yield path, element
