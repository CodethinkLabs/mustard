# Copyright (C) 2012 Codethink Limited


import markdown

import mustard


class Component(mustard.elementfactory.Element):

    def __init__(self, data):
        mustard.elementfactory.Element.__init__(self, data)

        self.architecture = None
        self.interfaces = {}
        self.tests = {}
        
        self.mapped_here = {}
        for ref in data.get('mapped-here', []):
            self.mapped_here[ref] = None

    def get_children(self):
        children = []
        if self.architecture:
            children.append(self.architecture)
        for path, item in self.work_items.iteritems():
            if item:
                children.append((path, item))
        for path, interface in self.interfaces.iteritems():
            if interface:
                children.append((path, interface))
        for path, test in self.tests.iteritems():
            if test:
                children.append((path, test))
        return children
