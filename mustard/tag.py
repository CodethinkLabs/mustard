# Copyright (C) 2012 Codethink Limited


import markdown

import mustard


class Tag(mustard.elementfactory.Element):

    def __init__(self, data):
        mustard.elementfactory.Element.__init__(self, data)

        self.tagged = {}

    def tagged_by_title(self):
        tagged = list(self.tagged.iteritems())
        return mustard.sorting.sort_elements(tagged, {'sort_by': 'title'})
