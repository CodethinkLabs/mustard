# Copyright (C) 2012 Codethink Limited


import markdown

import mustard


class Architecture(mustard.elementfactory.Element):

    def __init__(self, data):
        mustard.elementfactory.Element.__init__(self, data)

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
        if self.integration_strategy[1]:
            children.append(self.integration_strategy)
        return children
