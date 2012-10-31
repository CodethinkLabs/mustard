# Copyright (C) 2012 Codethink Limited


import markdown

import mustard


class Component(mustard.elementfactory.Element):

    def __init__(self, data):
        mustard.elementfactory.Element.__init__(self, data)

        self.parent_architecture = data.get('architecture', None)
        self.architecture = None
        
        self.covers = {}
        for ref in data.get('covers', []):
            self.covers[ref] = None
