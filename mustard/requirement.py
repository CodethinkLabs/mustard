# Copyright (C) 2012 Codethink Limited


import markdown

import mustard


class Requirement(mustard.elementfactory.Element):

    def __init__(self, data):
        mustard.elementfactory.Element.__init__(self, data)

        self.covered_by = {}

        self.parent_requirements = {}
        if 'parent-requirements' in data:
            for parent in data['parent-requirements']:
                self.parent_requirements[parent] = None

        self.sub_requirements = {}
