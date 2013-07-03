# Copyright (C) 2012 Codethink Limited


import markdown

import mustard


class Component(mustard.elementfactory.Element):

    def __init__(self, data):
        mustard.elementfactory.Element.__init__(self, data)

        self.interfaces = {}
        self.verificationcriteria = {}
        
        self.components = {}
        self.integration_strategy = (None, None)
        self.toplevel = data.get('toplevel', False)

        self.mapped_here = {}
        for ref in data.get('mapped-here', []):
            self.mapped_here[ref] = None

    def get_children(self):
        children = []
        for path, item in self.work_items.iteritems():
            if item:
                children.append((path, item))
        for path, component in self.components.iteritems():
            if component:
                children.append((path, component))
        for path, interface in self.interfaces.iteritems():
            if interface:
                children.append((path, interface))
        for path, criterion in self.verificationcriteria.iteritems():
            if criterion:
                children.append((path, criterion))
        if self.integration_strategy[1]:
            children.append(self.integration_strategy)
        return children

    def sort_subcomponents(self, **kwargs):
        return mustard.sorting.sort_elements(self.components.items(), kwargs)
