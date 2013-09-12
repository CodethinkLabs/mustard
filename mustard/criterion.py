# Copyright (C) 2012 Codethink Limited


import markdown

import mustard


class VerificationCriterion(mustard.elementfactory.Element):

    def __init__(self, data):
        mustard.elementfactory.Element.__init__(self, data)

        self.mapped_here = {}
        for ref in data.get('mapped-here', []):
            self.mapped_here[ref] = None

    def is_toplevel(self):
        return True

    def get_children(self):
        children = []
        return children
