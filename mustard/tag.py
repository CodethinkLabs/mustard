# Copyright (C) 2012 Codethink Limited


import markdown

import mustard


class Tag(mustard.elementfactory.Element):

    def __init__(self, data):
        mustard.elementfactory.Element.__init__(self, data)

        self.tagged = {}

    def is_toplevel(self):
        return True

    def sorted_tagged(self):
        tagged = list(self.tagged.iteritems())
        return mustard.sorting.sort_elements(tagged, {'sort_by': 'DEFAULT'})
