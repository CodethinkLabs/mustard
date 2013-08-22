# Copyright (C) 2012 Codethink Limited


import mustard


class WorkItem(mustard.elementfactory.Element):

    def __init__(self, data):
        mustard.elementfactory.Element.__init__(self, data)

        self.parents = {}
        for ref in data.get('parents', None) or []:
            if ref:
                self.parents[ref] = None

        self.mapped_here = {}
        for ref in data.get('mapped-here', []):
            self.mapped_here[ref] = None

        self.work_items = {}

    def get_children(self):
        return self.work_items.items()

    def sort_work_items(self, **kwargs):
        return mustard.sorting.sort_elements(self.work_items.items(), kwargs)
