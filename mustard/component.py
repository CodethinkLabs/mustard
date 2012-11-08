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
