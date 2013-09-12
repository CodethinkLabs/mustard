# Copyright (C) 2012 Codethink Limited


import markdown

import mustard


class IntegrationStrategy(mustard.elementfactory.Element):

    def __init__(self, data):
        mustard.elementfactory.Element.__init__(self, data)

        self.verificationcriteria = {}

        self.mapped_here = {}
        for ref in data.get('mapped-here', []):
            self.mapped_here[ref] = None

    def is_toplevel(self):
        return True

    def get_children(self):
        children = []
        for path, item in self.work_items.iteritems():
            if item:
                children.append((path, item))
        for path, criterion in self.verificationcriteria.iteritems():
            if criterion:
                children.append((path, criterion))
        return children
