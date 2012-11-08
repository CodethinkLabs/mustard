# Copyright (C) 2012 Codethink Limited


import markdown

import mustard


class WorkItem(mustard.elementfactory.Element):

    def __init__(self, data):
        mustard.elementfactory.Element.__init__(self, data)

        self.parents = {}
        for ref in data.get('parents', None) or []:
            if ref:
                self.parents[ref] = None
